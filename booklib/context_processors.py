from datetime import date, timedelta
from django.db.models import Count, Q
from .models import Book

def top_books(request):
    # Считаем только за последние 90 дней
    date_past = date.today() - timedelta(days=90)

    # Аннотируем книги: количество выдач и используем поле rating
    books = (
        Book.objects.prefetch_related('fotoregistr_set', 'author_set', 'genres')
        .annotate(
            order_count=Count(
                'bookobj__order',
                filter=Q(bookobj__order__distrib_date__gte=date_past),
                distinct=True
            )
        )
        .order_by('-order_count', '-rating')[:3]   # сортировка по двум критериям
    )

    # Делаем список [[count, book], ...]
    list_books = [[book.order_count, book] for book in books]

    return {
        'list_books': list_books,
        'show_rating': True,
    }