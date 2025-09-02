from django.contrib import admin

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

# class OrderAdmin(admin.ModelAdmin):
#     pass
    # list_display = ('distrib_date', 'quantity_books', 'status_order')
    # search_fields = ('distrib_date', 'status_order')
    # ordering = ('distrib_date', 'status_order')

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
admin.site.register(Order)
admin.site.register(ReturnB, ReturnBAdmin)

