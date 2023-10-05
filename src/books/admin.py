from django.contrib import admin
from books import models

# admin.site.register(models.Cart)

# admin.site.register(models.CustomerRating)

admin.site.register(models.OrderHistory)

class BooksAdmin(admin.ModelAdmin):
    list_display =('title','author','genre','price','quantity')
    list_filter = ('status',)
    search_fields = ['title','author','genre']
    prepopulated_fields = {'slug':('title',)}

class GenreAdmin(admin.ModelAdmin):
    list_display =('name',)
    prepopulated_fields = {'slug':('name',)}

admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Book, BooksAdmin)
