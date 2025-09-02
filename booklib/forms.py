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
    sp_years = [(str(y), str(y)) for y in range(date.today().year, 1000, -1)]

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
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple()
    )
    photo_book = forms.ImageField(
        label='Фото обложки',
        required=True
    )
    name_author1 = forms.CharField(
        label='Автор1',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите автора1'})
    )
    photo_author1 = forms.ImageField(
        label='Фото автора1',
        required = False
    )
    name_author2 = forms.CharField(
        label='Автор2',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите автора2'})
    )
    photo_author2 = forms.ImageField(
        label='Фото автора2',
        required = False
    )
    name_author3 = forms.CharField(
        label='Автор3',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите автора3'})
    )
    photo_author3 = forms.ImageField(
        label='Фото автора3',
        required = False
    )
    year = forms.ChoiceField(
        label='Год издания',
        choices=sp_years,
        widget=forms.Select()
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
            'min': '0.01',
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
    quantity = forms.IntegerField(
        label='Количество книг',
        initial = 1,
        widget=forms.NumberInput(attrs={'min':1, 'step':1, 'placeholder':'Введите количество книг'})
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
            ),'first_name': forms.TextInput(
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

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name_genre']
        labels = {'name_genre': ''}
