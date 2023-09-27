from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .models import Book, Cart, Order, CustomerRating, ShippingAddress
from django.db.models import Q
from django.core.paginator import Paginator, Page
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import *


def homeView(request):
    books = Book.objects.all()
    paginator = Paginator(books, 9)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    genre = Book.objects.values('genre').distinct().order_by('genre')
    context = {'books': books, 'genre':genre}
    search_book = request.GET.get('search')
    if search_book:
        books = Book.objects.filter(Q(title__icontains=search_book)).distinct()
        paginator = Paginator(books, 9)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        genre = Book.objects.values('genre').distinct().order_by('genre')
        if not books:
            books = Book.objects.all()
            paginator = Paginator(books, 9)
            page = request.GET.get('page')
            books = paginator.get_page(page)
            error_message = "No Stories found try something else!"
            return render(request, 'index.html', {'error_message': error_message, 'books': books, 'genre':genre})
        return render(request,'index.html',{'books': books,'genre':genre })
    return render(request, 'index.html', context)

def categoryView(request, cats):
    category_post = Book.objects.filter(genre=cats)
    genre = Book.objects.values('genre').distinct().order_by('genre')
    context = {'category_post':category_post, 'genre':genre}
    return render(request, 'category.html',context)



def bookDetail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    genre = Book.objects.values('genre').distinct().order_by('genre')
    context = {'book': book, 'genre':genre}
    return render(request, 'book-detail.html', context)
    
@login_required
def submitRating(request, book_id):
    if request.method == 'POST':
        rating_value = float(request.POST.get('rating'))
        book = get_object_or_404(Book, pk=book_id)
        existing_rating = CustomerRating.objects.filter(user=request.user, book=book).first()
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
        else:
            new_rating = CustomerRating(user=request.user, book=book, rating=rating_value)
            new_rating.save()
        average_rating = CustomerRating.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
        book.average_rating = average_rating
        book.save()
    return redirect('book_detail', book_id=book_id)



@login_required
def cartView(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = calculateCartTotal(cart_items)
    form = UpdateCartForm()
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'form': form,
    }
    return render(request, 'shopping/cart.html', context)

def calculateCartTotal(cart_items):
    total = 0
    for item in cart_items:
        total += item.books.price * item.quantity
    return total

@login_required
def cartUpdate(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if request.method == 'POST':
        form = UpdateCartForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
    return redirect('cart')

@login_required
def cartRemove(request, item_id):
    cart_item_to_remove = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item_to_remove.delete()
    return redirect('cart')

def checkoutView(request):
    context = {}
    return render(request, 'index.html', context)