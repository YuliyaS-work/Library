from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date, datetime
import uuid

from .forms import PersonForm, BookForm
from .models import Book, BookObj, FotoRegistr, Author, Order, Person, ReturnB


def get_main_page(request):
    '''Начальная страница.'''
    books = Book.objects.prefetch_related('books', 'fotoregistr_set', 'author_set', 'genres').all()
    context={'books':books}
    return render(request, 'main_page.html', context)

def get_new_book(request):
    '''Регистрация новой книги.'''
    formB = BookForm()
    if request.method == 'POST':
        formB = BookForm(request.POST, request.FILES)
        if formB.is_valid():
            cleaned_data = formB.cleaned_data
            title_rus = cleaned_data.get('title_rus')
            title_orig = cleaned_data.get('title_orig')
            name_genre = cleaned_data.get('name_genre')
            photo_book = cleaned_data.get('photo_book')
            name_author1 = cleaned_data.get('name_author1')
            photo_author1 = cleaned_data.get('photo_author1')
            name_author2 = cleaned_data.get('name_author2')
            photo_author2 = cleaned_data.get('photo_author2')
            name_author3 = cleaned_data.get('name_author3')
            photo_author3 = cleaned_data.get('photo_author3')
            year = cleaned_data.get('year')
            quantity_pages = cleaned_data.get('quantity_pages')
            registr_date = cleaned_data.get('registr_date')
            price = cleaned_data.get('price')
            price_per_day = cleaned_data.get('price_per_day')
            coefficient = cleaned_data.get('coefficient')
            space = cleaned_data.get('space')

            existing_book = Book.objects.filter(
                title_rus=title_rus,
                title_orig=title_orig,
                year=year,
                quantity_pages=quantity_pages
            )
            if existing_book.exists():
                book = existing_book.first()
                book_obj = BookObj.objects.create(
                    book=book,
                    registr_date=registr_date,
                    price=price,
                    price_per_day=price_per_day,
                    coefficient=coefficient,
                    space=space
                )
            else:
                book = Book.objects.create(
                    title_rus=title_rus,
                    title_orig=title_orig,
                    year=year,
                    quantity_pages=quantity_pages
                )
                book.genres.set(name_genre)

                book_obj = BookObj.objects.create(
                    book=book,
                    registr_date=registr_date,
                    price=price,
                    price_per_day=price_per_day,
                    coefficient=coefficient,
                    space=space
                )
                foto_registr = FotoRegistr.objects.create(books=book, photo_book=photo_book)

                author_spisok = []
                author_spisok_name = [name_author1, name_author2, name_author3]
                author_spisok_photo = [photo_author1, photo_author2, photo_author3]
                for index, author in enumerate(author_spisok_name):
                    author_q, created = Author.objects.update_or_create(name=author,
                                                                        defaults={'photo_author': author_spisok_photo[index]})
                    author_spisok.append(author_q)
                book.author_set.set(author_spisok)

            book.update_general_quantity()
            book.get_current_quantity()
            book.save()
            return redirect('/lib/add_book/')
        else:
            print(formB.errors)
    context = {'formB':formB}
    return render(request, 'add_book.html', context)


def get_new_person(request):
    '''Регистрация нового читателя.'''
    formP = PersonForm()
    if request.method == 'POST':
        formP = PersonForm(request.POST)
        if formP.is_valid():
            formP.save()
            return redirect('/lib/add_person')
        else:
            print(formP.errors)

    context = {'formP':formP}
    return render(request, 'add_person.html', context)


def give_book(request):
    '''Выдача книги.'''
    books = Book.objects.filter(current_quantity__gt=0)
    persons = Person.objects.filter(quantity_books__lt=5)
    if request.method == 'POST':
        person_id = request.POST.get('person')
        person = Person.objects.get(pk=person_id)
        person.quantity_books += int(request.POST.get('quantity_books'))
        person.save()

        order = Order(
            person = person,
            quantity_books = request.POST.get('quantity_books'),
            distrib_date = date.today(),
            pre_return_date = datetime.strptime(request.POST.get('pre_return_date'),"%Y-%m-%d"),
            pre_cost = request.POST.get('pre_cost'),
            status_order = True
        )
        order.save()

        book_list = []
        for i in range(1,6):
            try:
                bookobj_registr_number = request.POST.get(f'bookobj_{i}')
                registr_number = uuid.UUID(bookobj_registr_number)
                bookobj = BookObj.objects.get(registr_number=registr_number)
                bookobj.status_book = True
                bookobj.save(update_fields = ['status_book'])
                book_list.append(bookobj)

                book_id = request.POST.get(f'book_{i}')
                book = Book.objects.get(pk=book_id)
                book.distrib_quantity += 1
                book.get_current_quantity()
                book.save(update_fields = ['distrib_quantity', 'current_quantity'])
            except 	ValueError:
                pass
        order.book_obj.set(book_list)
        order.save()

        returnB = ReturnB(
            order=order
        )
        returnB.save()

    context = {'books':books, 'persons':persons}
    return render(request, 'give_book.html', context)


def get_bookobj(request):
    '''Загружает физические экземпляры книги при выдаче. '''
    book_id = request.GET.get('book_id')
    print(f"Book_id: {book_id}")
    bookobjs = BookObj.objects.filter(book_id=book_id, status_book=0)
    data = []
    for obj in bookobjs:
        data.append({
            "registr_number": obj.registr_number,
            "price_per_day": float(obj.price_per_day)
        })
    return JsonResponse(data, safe=False)
