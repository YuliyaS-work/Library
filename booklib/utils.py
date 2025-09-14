# для проверки работы строка 23, иначе 23 удалить, 11 раскомментить

from datetime import datetime
from django.core.mail import send_mail

from booklib.models import Person


def send_debt_email():
    '''Выполняет отправку писем читателям, у кооторых истек срок выдачи книг.'''
    # today = datetime.today().date()

    persons = Person.objects.filter(debt__gt=0)
    print(f' найден {persons}')

    for person in persons:
        data_books = []
        orders = person.order_set.filter(status_order=1)
        print(orders)
        for order in orders:

            # для проверки работы, иначе 22 удалить, 10 раскомментить
            today = order.pre_return_date
            if today == order.pre_return_date:
                returnbs = order.returnb_set.all()
                rbooks1 = []
                bookobjs1 = []
                for returnb in returnbs:
                    rbooks2 = list(returnb.bookobj_set.all())
                    rbooks1.extend(rbooks2)
                bookobjs = list(order.book_obj.all())
                for bb in bookobjs:
                    if bb not in rbooks1:
                        bookobjs1.append(bb)
                books_data = [(bookobj.book.title_rus, f" номер {bookobj.registr_number}") for bookobj in bookobjs1]
                data_books.append({"Выдача":order, "Книги":books_data})
                print(data_books)
        if data_books:
            subject = 'Debt'
            message = (f'Здравствуйте, {person.first_name} {person.surname}! Истек срок выдачи книг. Не забудьте, пожалуйста, вернуть книги {data_books} и оплатить.')
            print(message)
            recipient_list = ['by-40yuliya@yandex.by']

            try:
                send_mail(subject, message, None, recipient_list=recipient_list, fail_silently=False)

            except Exception:
                print(f'Ошибка при отправке письма')

