import sqlite3
import psycopg2

# Подключение к SQLite
sqlite_conn = sqlite3.connect('lib.db')
sqlite_cursor = sqlite_conn.cursor()

# Подключение к PostgreSQL
pg_conn = psycopg2.connect(
    dbname='lib',
    user='admin',
    password='admin',
    host='localhost',
    port='5432'
)
pg_cursor = pg_conn.cursor()

# Получение списка таблиц из SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table_name in tables:
    table_name = table_name[0]
    # Получение схемы таблицы из SQLite
    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    columns_info = sqlite_cursor.fetchall()

    # Формируем CREATE TABLE для PostgreSQL
    columns_definitions = []
    for col in columns_info:
        col_name = col[1]
        col_type = col[2]
        # Простая замена типов данных
        if 'INT' in col_type.upper():
            col_type = 'INTEGER'
        elif 'CHAR' in col_type.upper() or 'TEXT' in col_type.upper():
            col_type = 'TEXT'
        elif 'BLOB' in col_type.upper():
            col_type = 'BYTEA'
        elif 'REAL' in col_type.upper() or 'FLOA' in col_type.upper() or 'DOUB' in col_type.upper():
            col_type = 'REAL'
        else:
            col_type = 'TEXT'  # по умолчанию

        # Проверка, является ли колонка первичным ключом
        if col[5] == 1:
            col_type = 'SERIAL PRIMARY KEY' if 'INTEGER' in col_type else col_type

        columns_definitions.append(f"{col_name} {col_type}")

    create_table_sql = f"CREATE TABLE {table_name} ({', '.join(columns_definitions)});"
    print(f"Создаем таблицу: {create_table_sql}")
    pg_cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
    pg_cursor.execute(create_table_sql)

    # Перенос данных
    sqlite_cursor.execute(f"SELECT * FROM {table_name};")
    rows = sqlite_cursor.fetchall()

    if rows:
        placeholders = ', '.join(['%s'] * len(rows[0]))
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders});"
        for row in rows:
            pg_cursor.execute(insert_sql, row)

# Сохраняем изменения
pg_conn.commit()

# Закрываем соединения
sqlite_conn.close()
pg_cursor.close()
pg_conn.close()

print("Миграция завершена.")