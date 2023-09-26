from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .models import Book, Customer, Cart, Order, CustomerRating, ShippingAddress
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def homeView(request):
    books = Book.objects.all()
    paginator = Paginator(books, 9)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    context = {'books': books}
    search_book = request.GET.get('search')
    if search_book:
        books = Book.objects.filter(Q(title__icontains=search_book)).distinct()
        return render(request,'index.html',{'books': books })
    return render(request, 'index.html', {'books': books})

def categoryView(request, cats):
    category_post = Book.objects.filter(genre=cats)
    return render(request, 'category.html',{'cats':cats.id(),'category_post':category_post})


def bookDetail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {'book': book}
    return render(request, 'book-detail.html', context)
    
@login_required
def submitRating(request, book_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
    return redirect('book_detail', book_id=book_id)



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

