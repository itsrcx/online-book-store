from django.contrib import admin
import books import models

admin.site.register(models.Category)

class BooksAdmin(admin.ModelAdmin):
    list_display =('title','category','price','quantity')
    list_filter = ('status',)
    search_fields = ['title','category']
    # prepopulated_fields = {'slug':['title']}

admin.site.register(models.Books, BooksAdmin)
