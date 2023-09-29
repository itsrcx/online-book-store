from django.contrib import admin
from books import models

# admin.site.register(models.Cart)

# admin.site.register(models.CustomerRating)

admin.site.register(models.OrderHistory)

class BooksAdmin(admin.ModelAdmin):
    list_display =('title','author','genre','price','quantity','average_rating')
    list_filter = ('status',)
    search_fields = ['title','author','genre']
    # prepopulated_fields = {}

admin.site.register(models.Book, BooksAdmin)
