with open('data.json', 'r', encoding='cp1251') as f_in:
    content = f_in.read()

with open('data_utf8.json', 'w', encoding='utf-8') as f_out:
    f_out.write(content)