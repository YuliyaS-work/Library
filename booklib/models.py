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
    rating = models.DecimalField('Общий рейтинг', max_digits=2, decimal_places=1, null=True, blank=True)
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
    coefficient = models.DecimalField('Коэффициент', max_digits=2, decimal_places=1, choices=coef, default=1, null=True, blank=True)
    space = models.CharField('Место хранения', max_length=200, null=True, blank=True)
    status_book = models.BooleanField('Статус книги', default=False)

    class Meta:
        verbose_name='Экземпляр книги'
        verbose_name_plural='Экземпляры книг'

    def __str__(self):
        return f'{self.book.title_rus} {self.registr_number}'

    @property
    def current_price_per_day(self):
        '''Определяет стоимость книги за день.'''
        return self.price_per_day * self.coefficient

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
        self.debt = ReturnB.objects.filter(status_returnb=False).aggregate(debt=Sum('debt_order'))['debt']
        return self.debt_order


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
    penalty = models.DecimalField('Пеня за день', max_digits=5, decimal_places=2, null=True,blank=True)

    class Meta:
        verbose_name = 'Ордер'
        verbose_name_plural = 'Ордера'

    def __str__(self):
        return f'{self.person.last_name}'


    def get_penalty(self):
        self.penalty = 0.01 * self.pre_cost
        return self.penalty

    def get_debt(self):
        self.debt_order = ReturnB.objects.filter(status_returnb=False).aggregate(debt=Sum('return_cost'))['debt']
        return self.debt_order


class ReturnB(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Выдача')
    return_date = models.DateField('Дата возврата', auto_now=True, null=True,blank=True)
    return_cost = models.DecimalField('Стоимость возврата', max_digits=5, decimal_places=2, null=True,blank=True)
    status_returnb = models.BooleanField('Наличие задолженности', default=False)

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'

    def __str__(self):
        return f'{self.return_date}'

    @property
    def days(self):
        '''Рассчитывает количество дней использования книги.'''
        return  self.return_date - self.order.distrib_date

    def get_return_cost(self, d=30):
        quantity = self.order.quantity_books
        price_per_day = self.order.book_obj.price_per_day
        penalty_per_day = self.order.penalty
        total_cost = price_per_day * self.days
        total_pre_cost = price_per_day * d
        if self.days <= 30:
            if quantity <= 2:
                self.return_cost = total_cost
            elif 2 < quantity < 5:
                self.return_cost = 0.9 * total_cost  # вопрос к округлению (функция round(f, 2))
            elif quantity == 5:
                self.return_cost = 0.85 * total_cost
        elif 30 < self.days <= 120:
            penalty = penalty_per_day * (self.days - 30)
            if quantity <= 2:
                self.return_cost = total_pre_cost + penalty
            elif 2 < quantity < 5:
                self.return_cost = 0.9 * total_pre_cost + penalty  # вопрос к округлению (функция round(f, 2))
            elif quantity == 5:
                self.return_cost = 0.85 * total_pre_cost * d + penalty
        return self.return_cost

