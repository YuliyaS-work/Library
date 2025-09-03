from django.contrib import admin
from django import forms

from .models import Book, Person, BookObj, Order, ReturnB, Genre, Author, FotoStatus, FotoRegistr

class BookAdmin(admin.ModelAdmin):
    list_display = ('title_rus',)
    ordering = ('title_rus',)
    search_fields = ('title_rus',)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'mail')
    ordering = ('last_name', )
    search_fields = ('last_name', 'first_name', 'date_of_birth', 'mail')

class BookObjAdmin(admin.ModelAdmin):
    list_display = ('registr_number',)
    search_fields = ('registr_number',)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name_genre',)
    search_fields = ('name_genre',)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class FotoRegistrAdmin(admin.ModelAdmin):
    list_display = ('photo_book',)
    search_fields = ('photo_book',)

class FotoStatusAdmin(admin.ModelAdmin):
    list_display = ('photo_status', 'list_status')
    search_fields = ('photo_status',)

class OrderFormAdmin(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['book_obj'].queryset = BookObj.objects.all()
        else:
            self.fields['book_obj'].queryset = BookObj.objects.filter(status_book=False)


class OrderAdmin(admin.ModelAdmin):
    form = OrderFormAdmin
    list_display = ('distrib_date', 'quantity_books', 'status_order')
    list_filter = ('distrib_date', 'status_order')
    search_fields = ('status_order',)
    ordering = ('distrib_date', 'status_order')

class ReturnBAdmin(admin.ModelAdmin):
    list_display = ('return_date', 'status_returnb', 'return_cost')
    search_fields = ('return_date', 'status_returnb')
    ordering = ('return_date', 'status_returnb')


admin.site.register(Book, BookAdmin)
admin.site.register(BookObj, BookObjAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(FotoRegistr, FotoRegistrAdmin)
admin.site.register(FotoStatus, FotoStatusAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ReturnB, ReturnBAdmin)

