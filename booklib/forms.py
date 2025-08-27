from datetime import date
from django import forms

from .models import Book, BookObj, Genre, Author, Person


class BookForm(forms.Form):
    coef = (
        (1, 'отличное'),
        (0.8, 'хорошее'),
        (0.6, 'удовлетворительное'),
        (0.4, 'неудовлетворительное'),
        (0.2, 'списание'),
    )
    title_rus = forms.CharField(
        label='Наименование книги',
        required=True
    )
    title_orig = forms.CharField(
        label='Наименование книги (ориг.)',
        required=False
    )
    name_genre = forms.ModelMultipleChoiceField(
        label='Жанр',
        required=True,
        queryset=Genre.objects.all()
    )
    photo_book = forms.ImageField(
        label='Фото обложки',
        required=True
    )
    name_authors = forms.CharField(
        label='Авторы',
        required=True,
    )
    photo_author = forms.ImageField(
        label='Фото авторов',
        required = False
    )
    year = forms.IntegerField(
        label='Год издания',
        min_value=1,
        required=False
    )
    quantity_pages = forms.IntegerField(
        label='Количество страниц',
        required=False,
        min_value=0,
    )
    price = forms.DecimalField(
        label='Стоимость',
        required=True
    )
    price_per_day = forms.DecimalField(
        label='Цена за день',
        required=True
    )
    coefficient = forms.ChoiceField(
        label='Коэффициент',
        choices=coef,
        initial=1,
        widget=forms.Select(),
        required=False
    )
    registr_date = forms.DateField(
        label='Дата регистрации',
        required=True,
        initial=date.today
    )
    space = forms.CharField(
        label='Место хранения',
        required=False
    )


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('last_name', 'first_name', 'surname', 'date_of_birth',
                  'address', 'passport', 'mail', 'agreement')
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}


class OrderFrom(forms.Form):
    b_range = (
        ('--', 'Выберите количество'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        label='Получатель книги',
        required=True
    )
    book1= forms.ModelChoiceField(
        queryset=Book.objects.exclude(current_quantity=0),
        label='Книги для выдачи',
        required=True
    )
    book2 = forms.ModelChoiceField(
        queryset=Book.objects.exclude(current_quantity=0),
        label='Книги для выдачи',
        required=False
    )
    book3 = forms.ModelChoiceField(
        queryset=Book.objects.exclude(current_quantity=0),
        label='Книги для выдачи',
        required=False
    )
    book4 = forms.ModelChoiceField(
        queryset=Book.objects.exclude(current_quantity=0),
        label='Книги для выдачи',
        required=False
    )
    book5 = forms.ModelChoiceField(
        queryset=Book.objects.exclude(current_quantity=0),
        label='Книги для выдачи',
        required=False
    )
    quantity_books = forms.ChoiceField(
        label='Количество выданных книг',
        choices=b_range,
        initial='--',
        widget=forms.Select(),
        required=True
    )
    pre_return_date = forms.DateField(
        label='Дата возврата',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'required-field'})
    )
    distrib_date = forms.DateField(
        label='Дата выдачи',
        required=True,
        initial=date.today
    )

