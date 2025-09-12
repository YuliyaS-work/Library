from datetime import date

from django.core.validators import RegexValidator
from django.db import models
import uuid
from django.db.models import Sum



class Book(models.Model):
    '''Книги в библиотеке.'''
    rating_book = (
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, "\U00002605"),
    )
    title_rus = models.CharField('Наименование книги', max_length=200)
    title_orig = models.CharField('Наименование книги (ориг.)', max_length=200, null=True, blank=True)
    year = models.PositiveIntegerField('Год издания', null=True,blank=True)
    quantity_pages = models.PositiveIntegerField('Количество страниц',null=True,blank=True)
    rating = models.DecimalField('Общий рейтинг', max_digits=2, decimal_places=1, default=0)
    counter_rating = models.DecimalField('Счетчик рейтинга', max_digits=2, decimal_places=1, default=0, null=True, blank=True)
    return_rating = models.DecimalField('Рейтинг при возврате', max_digits=2, decimal_places=1, choices = rating_book, null=True, blank=True)
    general_quantity = models.IntegerField('Общее количество экземпляров', default=0, null=True, blank=True)
    current_quantity = models.IntegerField('Доступное количество экземпляров', null=True, blank=True)
    distrib_quantity = models.IntegerField('Количество выданных экземпляров', default=0, null=True, blank=True)
    genres = models.ManyToManyField('Genre')
    class Meta:
        verbose_name='Книга'
        verbose_name_plural='Книги'
        ordering = ['current_quantity', 'title_rus']

    def __str__(self):
        return f'{self.title_rus}, {self.year}'

    def count_rating(self):
        '''Расчитывает рейтин книгию'''
        self.rating = round((self.rating * self.counter_rating + self.return_rating) / ( self.counter_rating + 1 ), 1)
        return self.rating

    def update_general_quantity(self):
        '''Обновляет общее количество книг.'''
        self.general_quantity = self.general_quantity + 1
        return self.general_quantity

    def get_current_quantity(self):
        '''Определяет количество доступных книг.'''
        self.current_quantity = self.general_quantity - self.distrib_quantity
        return self.current_quantity


class BookObj(models.Model):
    '''Пул книг одного вида.'''
    coef = (
        (1, 'отличное'),
        (0.8, 'хорошее'),
        (0.6, 'удовлетворительное'),
        (0.4, 'неудовлетворительное'),
        (0.2, 'списание'),
    )
    registr_number = models.UUIDField('Регистрационный номер', primary_key=True, default=uuid.uuid4, editable=False, max_length=8)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name='Книга')
    registr_date = models.DateField('Дата регистрации', auto_now_add=True)
    price = models.DecimalField('Стоимость', max_digits=8, decimal_places=2)
    price_per_day = models.DecimalField('Цена за день', max_digits=5, decimal_places=2)
    current_day_price = models.DecimalField('Текущая цена за день', max_digits=5, decimal_places=2, null=True, blank=True)
    coefficient = models.DecimalField('Коэффициент', max_digits=2, decimal_places=1, choices=coef, default=1, null=True, blank=True)
    space = models.CharField('Место хранения', max_length=200, null=True, blank=True)
    status_book = models.BooleanField('Статус книги', default=False)
    return_order = models.ManyToManyField('ReturnB', verbose_name='Книги возврата')
    mark = models.BooleanField(default=False)

    class Meta:
        verbose_name='Экземпляр книги'
        verbose_name_plural='Экземпляры книг'

    def __str__(self):
        return f'{self.book.title_rus} {self.registr_number}'

    # def get_current_day_price(self):
    #     '''Определяет стоимость книги за день.'''
    #     self.current_day_price = round(float(self.price_per_day) * self.coefficient, 2)
    #     return self.current_day_price

    @property
    def current_final_price(self):
        '''Определяет остаточную стоимость книги'''
        return self.price * self.coefficient


class Genre(models.Model):
    '''Жанры книг.'''
    name_genre = models.CharField('Жанр', max_length=50, validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])

    class Meta:
        verbose_name='Жанр книги'
        verbose_name_plural='Жанры книг'

    def __str__(self):
        return self.name_genre


class Author(models.Model):
    '''Авторы книг.'''
    books = models.ManyToManyField(Book)
    name = models.CharField('Автор', max_length=200, validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    photo_author = models.ImageField('Фото авторов', upload_to='photo_author/', null=True, blank=True)

    class Meta:
        verbose_name='Автор книги'
        verbose_name_plural='Авторы книг'

    def __str__(self):
        return self.name


class FotoRegistr(models.Model):
    '''Фото обложки книги.'''
    books = models.ForeignKey(Book, on_delete=models.PROTECT)
    photo_book = models.ImageField('Фото обложки', upload_to='photo_book/')

    class Meta:
        verbose_name='Фотография обложки книги'
        verbose_name_plural='Фотографии обложки книг'

    def __str__(self):
        return f'Фото книги {self.books.title_rus}'

class FotoStatus(models.Model):
    '''Текущее состояние книги.'''
    book_obj = models.ForeignKey(BookObj, on_delete=models.PROTECT)
    photo_status = models.ImageField('Фото состояния книги', upload_to='photo_status/', null=True, blank=True)
    list_status = models.TextField('Описание', null=True, blank=True, max_length=1000)

    class Meta:
        verbose_name='Текущее состояние книги'
        verbose_name_plural='Текущие состояния книги'

    def __str__(self):
        return f'Состояние книги {self.book_obj.registr_number}'


class Person(models.Model):
    ''' Читатели библиотеки.'''
    last_name=models.CharField('Фамилия', max_length=50,  validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    first_name=models.CharField('Имя', max_length=50,  validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    surname=models.CharField('Отчество', max_length=50,null=True,blank=True,  validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    passport=models.CharField('Номер паспорта', max_length=50, null=True,blank=True, unique=True)
    date_of_birth=models.DateField('Дата рождения')
    address=models.CharField('Адрес проживания', max_length=200, null=True,blank=True)
    mail=models.EmailField('Электронная почта', unique=True)
    agreement = models.BooleanField('Соглашение', default=True)
    status_person = models.BooleanField('Статус читателя', default=False)
    debt = models.DecimalField('Задолженность читателя', max_digits=7, decimal_places=2,  default=0)
    quantity_books = models.PositiveIntegerField('Выданные книги', default=0)

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        ordering = ['last_name']

    def __str__(self):
        return f'{self.last_name},{self.date_of_birth}, выдано {self.quantity_books} книг'

    def get_debt(self):
        debt_sum = self.order_set.filter(status_order=True).aggregate(debt=Sum('debt_order'))['debt']
        self.debt = debt_sum or 0
        return self.debt


class Order(models.Model):
    '''Выдача книги.'''
    b_range = (
        (1, '1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
    )
    person = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name='Получатель книги')
    book_obj = models.ManyToManyField(BookObj, verbose_name='Книга для выдачи')
    distrib_date = models.DateField('Дата выдачи')
    pre_return_date = models.DateField('Дата возврата')
    pre_cost = models.DecimalField('Предварительная стоимость', max_digits=5, decimal_places=2, null=True,blank=True)
    quantity_books = models.PositiveIntegerField('Количество выданных книг', choices=b_range)
    debt_order = models.DecimalField('Задолженность по выдаче', max_digits=7, decimal_places=2, null=True,blank=True)
    status_order = models.BooleanField('Наличие задолженности', default=False)
    discount = models.DecimalField('Скидка', max_digits=3, decimal_places=2, null=True,blank=True)
    mark = models.BooleanField( default=False)

    class Meta:
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордера'

    def __str__(self):
        return f'{self.person.last_name} {self.person.date_of_birth}  номер выдачи {self.pk}'


    def get_debt_order(self):
        days_use = date.today() - self.distrib_date
        days = days_use.days
        # days = '20'
        books_return = []
        for returnb in self.returnb_set.all():
            spisok_books = list(returnb.bookobj_set.all())
            for book in spisok_books:
                books_return.append(book)
        books = []
        for book_order in self.book_obj.all():
            if book_order in books_return:
                pass
            else:
                books.append(book_order)
        summa = sum(book.current_day_price for book in books)
        if int(days) <= 30:
            debt_order = round(float(summa) * int(days) * float(self.discount), 2)
        elif 30 < int(days) <= 120:
            penalty = round(float(summa) * float(self.discount) * 1.01 * (int(days) - 30), 2)
            cost = round(float(summa) * 30 * float(self.discount), 2)
            debt_order = cost + penalty
            print(cost)
        self.debt_order = debt_order
        return self.debt_order


class ReturnB(models.Model):
    b_range = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Выдача')
    return_date = models.DateField('Дата возврата', auto_now=True, null=True,blank=True)
    return_cost = models.DecimalField('Стоимость возврата', max_digits=5, decimal_places=2, null=True,blank=True)
    quantity_book = models.PositiveIntegerField('Количество выданных книг', choices=b_range, null=True,blank=True)
    mark = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'

    def __str__(self):
        return f'{self.return_date}'


class Librarian(models.Model):
    username = models.CharField('Логин', max_length=20, unique=True)
    password = models.CharField('Пароль', max_length=256)
    status_user = models.BooleanField('Статус пользователя', default=0)
    last_login = models.DateTimeField('Дата входа', auto_now_add=True)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Библиотекарь'
        verbose_name_plural = 'Библиотекари'

    def __str__(self):
        return f'{self.username}'
