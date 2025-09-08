from django.shortcuts import render

from .models import Book, BookObj
from datetime import date, timedelta


def get_rait_page(request):
    books = Book.objects.all()
    dict_rait = {}
    date_past = date.today() - timedelta(days=90)

    for book in books:
        bookobjs = book.bookobj_set.all()
        counter =0
        for bookobj in bookobjs:
            count_order = bookobj.order_set.filter(distrib_date__gte= date_past ).all()
            length = len(list(count_order))
            counter += length
        dict_rait['book'] = counter

    for i, j in dict_rait.items():
        ...


    context = {}
    return render(request, 'raiting_book.html', context)