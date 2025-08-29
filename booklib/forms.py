from datetime import date, datetime
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
        widget=forms.TextInput(attrs={'placeholder': 'Введите название книги'})
    )
    title_orig = forms.CharField(
        label='Наименование книги (ориг.)',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите название книги(ориг.)'})
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
        widget=forms.TextInput(attrs={'placeholder': 'Введите название книги(ориг.)'})
    )
    photo_author = forms.ImageField(
        label='Фото авторов',
        required = False
    )
    year = forms.IntegerField(
        label='Год издания',
        max_value=date.today().year,
        required=False,
        error_messages={'invalid': 'Введите год в формате YYYY'},
        widget = forms.NumberInput(attrs={
            'pattern': r'\d{4}',
            'title': 'Введите год в формате YYYY',
            'placeholder': 'Введите год издания',
            'step': '1',
            'min': '1000',
            'max': str(date.today().year)})
    )
    quantity_pages = forms.IntegerField(
        label='Количество страниц',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'min': 1,
            'placeholder': 'Введите количество страниц',
            'style': 'width: 180px;'})
    )
    price = forms.DecimalField(
        label='Стоимость',
        required=True,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'placeholder': 'Введите стоимость книги',
            'style': 'width: 160px;'})
    )
    price_per_day = forms.DecimalField(
        label='Цена за день',
        required=True,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'min': '0',
            'placeholder': 'Введите стоимость книги',
            'style': 'width: 160px;'})
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
        initial=date.today(),
        widget=forms.DateInput(attrs={'readonly': 'readonly'})
    )
    space = forms.CharField(
        label='Место хранения',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите место хранения'})
    )


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('last_name', 'first_name', 'surname', 'date_of_birth',
                  'address', 'passport', 'mail', 'agreement')
        widgets = {
            'last_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'pattern': '[A-Za-zА-Яа-яЁё -]+',
                    'title': 'Можно использовать только буквы, пробелы и дефис',
                    'placeholder': 'Введите фамилию'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'pattern': '[A-Za-zА-Яа-яЁё -]+',
                    'title': 'Можно использовать только буквы, пробелы и дефис',
                    'placeholder': 'Введите имя'
                }
            ),
            'surname': forms.TextInput(
                attrs={
                    'type': 'text',
                    'pattern': '[A-Za-zА-Яа-яЁё -]+',
                    'title': 'Можно использовать только буквы, пробелы и дефис',
                    'placeholder': 'Введите отчество'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Введите адрес'
                }
            ),
            'passport': forms.TextInput(
                attrs={
                    'placeholder': 'Введите паспортные данные'}
            ),
            'mail': forms.EmailInput(
                attrs={
                    'placeholder': 'Введите адрес электронной почты'
                }
            )
        }



