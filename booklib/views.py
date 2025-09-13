from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Prefetch, F, Q
from django.db.models.functions import Lower
from datetime import date, datetime, timedelta
import uuid
import hashlib
import os
from .forms import LoginForm, RegisterForm
from .models import Librarian
from functools import wraps
from .forms import PersonForm, BookForm, GenreForm, ReturnForm1, ReturnForm2
from .models import Book, BookObj, FotoRegistr, Author, Order, Person, ReturnB, FotoStatus


def logout_user(request):
    if 'logout_button' in request.POST:
        request.session.flush()
        return redirect('login')
    return None

def librarian_login_required(fn):
    def wrapper(request, *args, **kwargs):
        if request.session.get('librarian_id'):
            return fn(request, *args, **kwargs)
        return redirect('login')
    return wrapper

@librarian_login_required
def get_main_page(request):
    '''Начальная страница с фильтром книг.'''
    # Проверка на logout
    logout_response = logout_user(request)
    if logout_response:
         return logout_response
    spisok_rait = []
    dict_rait = {}
    date_past = date.today() - timedelta(days=90)
    books = Book.objects.prefetch_related('bookobj_set', 'fotoregistr_set', 'author_set', 'genres').all()

    for book in books:
        bookobjs = book.bookobj_set.all()
        counter = 0
        for bookobj in bookobjs:
            count_order = bookobj.order_set.filter(distrib_date__gte=date_past).all()
            length = len(list(count_order))
            counter += length
        dict_rait[counter] = book.id

    for i, j in dict_rait.items():
        spisok_rait.append([i, j])
    spisok_rait.sort()
    spisok_rait.reverse()

    list_books = spisok_rait[:3]
    for sp in list_books:
        sp[1] = Book.objects.filter(pk=sp[1]).first()


    # Фильтры из GET-параметров
    query_title = request.GET.get('title', '').strip()
    query_author = request.GET.get('author', '').strip()
    query_genre = request.GET.get('genre', '').strip()
    query_year = request.GET.get('year', '').strip()

    if query_title:
        books = books.annotate(title_lower=Lower('title_rus')).filter(
            title_lower__contains=query_title.lower()
        )
    if query_author:
        books = books.annotate(author_lower=Lower('author__name')).filter(
            author_lower__contains=query_author.lower()
        )
    if query_genre:
        books = books.annotate(genre_lower=Lower('genres__name_genre')).filter(
            genre_lower__contains=query_genre.lower()
        )
    if query_year:
        books = books.filter(year=query_year)

    books = books.distinct()[:20]  # убираем дубли из-за join

    context = {
        'books': books,
        'query_title': query_title,
        'query_author': query_author,
        'query_genre': query_genre,
        'query_year': query_year,
        'list_books': list_books,
        'show_rating': True,  # добавляем флаг
    }

    return render(request, 'main_page.html', context)



@librarian_login_required
def get_new_book(request):
    '''Регистрация новой книги.'''
    logout_response = logout_user(request)
    if logout_response:
        return logout_response

    formB = BookForm()
    formG = GenreForm()
    if request.method == 'POST':
        if 'add_book' in request.POST:
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
                quantity = cleaned_data.get('quantity')


                existing_book = Book.objects.filter(
                    title_rus=title_rus,
                    title_orig=title_orig,
                    year=year,
                    quantity_pages=quantity_pages
                )
                for q in range( quantity):
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
                        print(type(price_per_day))
                        print(type(coefficient))
                        book_obj.current_day_price = round(float(book_obj.coefficient) * float(book_obj.price_per_day), 2)
                        book_obj.save(update_fields=['current_day_price'])
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
                        book_obj.current_day_price = round(float(book_obj.coefficient) * float(book_obj.price_per_day), 2)
                        book_obj.save(update_fields=['current_day_price'])

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
                    book.save(update_fields = ['general_quantity', 'current_quantity'])
                return redirect('/lib/add_book/')
            else:
                print(formB.errors)

        formG = GenreForm(request.POST)
        if 'add_genre' in request.POST:
            if formG.is_valid():
                formG.save()
                return redirect('/lib/add_book/')
            else:
                print(formG.errors)

    context = {'formB':formB, 'formG':formG}
    return render(request, 'add_book.html', context)

@librarian_login_required
def get_new_person(request):
    '''Регистрация нового читателя.'''

    logout_response = logout_user(request)
    if logout_response:
        return logout_response

    if request.method == 'POST':
        formP = PersonForm(request.POST)
        if formP.is_valid():
            formP.save()
            return redirect('/lib/add_person')
        else:
            print(formP.errors)
    else:
        formP = PersonForm()

    context = {'formP':formP}

    return render(request, 'add_person.html', context)

@librarian_login_required
def give_book(request):
    '''Выдача книги.'''

    logout_response = logout_user(request)
    if logout_response:
        return logout_response

    books = Book.objects.filter(current_quantity__gt=0)
    persons = Person.objects.filter(quantity_books__lt=5)
    pre_return_date = date.today() + timedelta(days=30)
    pre_return_date_str = pre_return_date.strftime('%Y-%m-%d')
    if request.method == 'POST':
        logout_user(request)
        person_id = request.POST.get('person')
        person = Person.objects.get(pk=person_id)
        if request.POST.get('quantity_books'):
            person.quantity_books += int(request.POST.get('quantity_books'))
            person.save()
        else:
            return redirect('give_book')

        order = Order(
            person = person,
            quantity_books = request.POST.get('quantity_books'),
            distrib_date = date.today(),
            # pre_return_date = datetime.strptime(request.POST.get('pre_return_date'),"%Y-%m-%d"),
            pre_return_date=pre_return_date_str,
            pre_cost = request.POST.get('pre_cost'),
            status_order = True,
            discount = request.POST.get('discount')
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
            except 	(ValueError, TypeError):
                pass
        order.book_obj.set(book_list)
        order.save()

        order.get_debt_order()
        order.save(update_fields=['debt_order'])

        person = order.person
        person.get_debt()
        person.save(update_fields=['debt'])

    context = {'books':books, 'persons':persons, 'pre_return_date':pre_return_date_str}
    return render(request, 'give_book.html', context)

def get_bookobj(request):
    '''Загружает физические экземпляры книги при выдаче. '''
    book_id = request.GET.get('book_id')
    bookobjs = BookObj.objects.filter(book_id=book_id, status_book=0)
    data = []
    for obj in bookobjs:
        data.append({
            "registr_number": obj.registr_number,
            "price_per_day": float(obj.current_day_price)
        })
    return JsonResponse(data, safe=False)

@librarian_login_required
def return_book(request):
    '''Оформляет возврат книг в библиотеку. Книги становятся доступными для выдачи.'''

    logout_response = logout_user(request)
    if logout_response:
        return logout_response

    formR1 = ReturnForm1()
    formR2 = ReturnForm2()
    book_list = []
    bookobj_list = []
    order = None
    cost = 0
    returnB = ReturnB()
    error = ''
    orderID=''

    if request.method == 'POST':
        logout_user(request)
        if 'data_books' in request.POST:
            formR1 = ReturnForm1(request.POST)
            if formR1.is_valid():
                cleaned_data = formR1.cleaned_data
                order = cleaned_data.get('order')
                try:
                    request.session['orderID']= order.id
                    bookobjs_order =order.book_obj.filter(status_book=True)
                    book_list=[BookObj.objects.filter(pk=b.pk) for b in bookobjs_order]
                    # print(book_list)
                except 	(AttributeError):
                    return redirect('/lib/return_book/')
            else:
                print(formR1.errors)

        formR2 = ReturnForm2(book_list=book_list)
        book_list=book_list
        # print(f'This {book_list}')

        if request.session.get('orderID'):
            orderID = request.session['orderID']
            # print(orderID)
        else:
            context = {'formR1': formR1, 'formR2': formR2, 'return_cost': cost, 'error': error}
            return render(request, 'return.html', context)
        order = Order.objects.get(pk=orderID)
        # print(order)

        if 'calculate' in request.POST:
            try:
                formR2 = ReturnForm2(request.POST, request.FILES, book_list=book_list)
                if formR2.is_valid():
                    cleaned_data = formR2.cleaned_data
                    # print(cleaned_data)
                    for index in range(6):
                        book_obj = request.POST.get(f'book_objs_{index}')
                        # print(type(book_obj))
                        # print(book_obj)
                        if book_obj == '':
                            pass
                        else:
                            coefficient = request.POST.get(f'coefficient_{index}')
                            # print(coefficient)
                            list_status = request.POST.get(f'list_status_{index}')
                            photo_status = request.POST.get(f'photo_status_{index}')
                            return_rating = request.POST.get(f'rating_{index}')

                            bookobj = BookObj.objects.filter(pk=book_obj).first()
                            # print(bookobj)
                            if bookobj:
                                bookobj.coefficient = coefficient
                                bookobj.status_book = False
                                bookobj.save(update_fields=['coefficient', 'status_book'])
                                # print(bookobj)
                                bookobj_list.append(bookobj)


                                foto_status = FotoStatus(book_obj=bookobj, list_status=list_status, photo_status=photo_status)
                                foto_status.save()
                                # print(foto_status)

                                if return_rating:
                                    bookobj.book.return_rating = return_rating
                                    # print(bookobj.book.return_rating)
                                    if bookobj.book.rating == 0:
                                        bookobj.book.rating = int(return_rating)
                                    else:
                                        rating = round((float(bookobj.book.rating) * int(bookobj.book.counter_rating) + int(bookobj.book.return_rating)) / (int(bookobj.book.counter_rating) + 1), 1)
                                        bookobj.book.rating = rating
                                    bookobj.book.counter_rating += 1
                                    bookobj.book.save(update_fields=['rating', 'counter_rating'])
                                bookobj.book.distrib_quantity = bookobj.book.distrib_quantity - 1
                                # print(bookobj.book.distrib_quantity)
                                bookobj.book.get_current_quantity()
                                # print(bookobj.book.current_quantity)
                                bookobj.book.save(update_fields=['rating', 'distrib_quantity', 'current_quantity'])
                                # print(bookobj.book)

                    quantity_book = cleaned_data.get('quantity_book')
                    # print(quantity_book)
                    return_date = cleaned_data.get('return_date')
                    returnB = ReturnB (order=order, return_date=return_date, quantity_book=quantity_book, mark=True)
                    returnB.save()
                    # print(returnB)

                    order.person.quantity_books = order.person.quantity_books - int(quantity_book)
                    # print(order.person.quantity_books)
                    order.person.save(update_fields=['quantity_books'])
                    # print(order.person.quantity_books)

                    # print(bookobj_list)
                    returnB.bookobj_set.set(bookobj_list)
                    # print(returnB.bookobj_set.all())

                    days_full = return_date - returnB.order.distrib_date
                    days = days_full.days
                    # days = '10'
                    # print(days)
                    summa = sum(book.current_day_price for book in returnB.bookobj_set.all())
                    # print(summa)
                    # print(returnB.order.discount)
                    if int(days)<=30:
                        return_cost = round(float(summa)*int(days)*float(returnB.order.discount), 2)
                    elif 30 < int(days) <= 120:
                        penalty = round(float(summa)*float(returnB.order.discount) * 1.01 * (int(days) - 30),2)
                        full_return_cost = round(float(summa)*30*float(returnB.order.discount), 2)
                        return_cost = full_return_cost + penalty
                    # print(return_cost)
                    returnB.return_cost = return_cost
                    returnB.save(update_fields=['return_cost'])
                    for book in bookobj_list:
                        book.current_day_price = round(float(book.coefficient) * float(book.price_per_day), 2)
                        book.save(update_fields=['current_day_price'])

                else:
                    print(formR2.errors)

                returnB = ReturnB.objects.filter(mark=True).first()
                # print(returnB)
                cost = returnB.return_cost
                # print(cost)
                #
                #
                #
                # print(type(order.quantity_books))
                # print(type(order.returnb_set.aggregate(Sum('quantity_book'))['quantity_book__sum']))
                if order.quantity_books == order.returnb_set.aggregate(Sum('quantity_book'))['quantity_book__sum']:
                    order.status_order = False
                    order.debt_order = 0
                    order.save(update_fields=['status_order', 'debt_order'])
                    print(order.status_order)

                returnB.mark = False
                returnB.save(update_fields=['mark'])

                order.get_debt_order()
                order.save(update_fields=['debt_order'])

                person = order.person
                person.get_debt()
                person.save(update_fields=['debt'])
            except (AttributeError, IntegrityError)	:
                return redirect('/lib/return_book/')
        if 'return' in request.POST:
            try:
                return redirect('/lib/return_book/')
            except AttributeError:
                return redirect('/lib/return_book/')


    context = {'formR1': formR1, 'formR2': formR2, 'return_cost': cost, 'error': error}
    return render(request, 'return.html', context)



def auth_user(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    login_error = ''
    register_error = ''
    show_register = False  # <-- флаг по умолчанию

    if request.method == 'POST':
        # Определяем, какая форма была отправлена по имени кнопки
        if 'login_submit' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                librarian = Librarian.objects.filter(username=username).first()

                def verify_password(stored_password, provided_password):
                    salt_hex = stored_password[:32]  # первые 16 байт = 32 символа
                    hash_hex = stored_password[32:]
                    salt = bytes.fromhex(salt_hex)
                    pwd_hash = hashlib.pbkdf2_hmac(
                        'sha256', provided_password.encode(), salt, 100000
                    )
                    return pwd_hash.hex() == hash_hex

                if librarian and verify_password(librarian.password, password):
                    request.session['librarian_id'] = librarian.id
                    return redirect('main')
                else:
                    login_error = 'Неверное имя пользователя или пароль'

        elif 'register_submit' in request.POST:
            register_form = RegisterForm(request.POST)
            show_register = True  # <-- переключаемся на форму регистрации
            if register_form.is_valid():
                username = register_form.cleaned_data.get('username')
                password1 = register_form.cleaned_data.get('password1')
                password2 = register_form.cleaned_data.get('password2')

                if Librarian.objects.filter(username=username).exists():
                    register_error = 'Пользователь с таким именем уже существует'
                elif password1 != password2:
                    register_error = 'Пароли не совпадают'
                else:
                    # Хешируем пароль
                    salt = os.urandom(16)
                    pwd_hash = hashlib.pbkdf2_hmac('sha256', password1.encode(), salt, 100000)
                    hashed = salt.hex() + pwd_hash.hex()

                    # Создаём пользователя
                    librarian = Librarian(username=username, password=hashed)
                    librarian.save()
                    return redirect('login')  # можно сразу показать страницу логина
            else:
                register_error = 'Проверьте корректность введённых данных'

    context = {
        'login_form': login_form,
        'form': register_form,
        'login_error': login_error,
        'register_error': register_error,
        'show_register': show_register,  # <-- передаём в шаблон
    }

    return render(request, 'login.html', context)


