from django.shortcuts import render
from django.views import generic
from .models import Book, Customer, Cart, Order, CustomerRating, ShippingAddress
from django.db.models import Q

def homeView(request):
    books = Book.objects.all()
    search_book = request.GET.get('search')
    if search_book:
        books = Book.objects.filter(Q(title__icontains=search_book)).distinct()
        return render(request,'index.html',{'books': books })
    return render(request, 'index.html', {'books': books})

def categoryView(request, cats):
    category_post = Book.objects.filter(genre=cats)
        return render(request, 'category.html',{'cats':cats.id(),'category_post':category_post})

def cartView(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        (order, created) = Orders.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # get all the child item for order class
    else:
        items = []

    context = {'items': items}
    return render(request, 'shopping/cart.html', context)

def checkoutView(request):
    context = {}
    return render(request, 'index.html', context)

