from django.shortcuts import redirect, render, get_object_or_404
from .models import Book, Cart, Order, CustomerRating, ShippingAddress, OrderHistory, Genre
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import *
from django.contrib import messages

def redirect_to_previous_page(request):
    referring_url = request.META.get('HTTP_REFERER')

    if referring_url:
        return redirect(referring_url)
    else:
        return redirect('home')

def homeView(request):
    books = Book.objects.all().order_by('title')
    paginator = Paginator(books, 9)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    genre = Genre.objects.all().order_by('name')
    context = {'books': books, 'genre':genre}
    search_book = request.GET.get('search')
    if search_book:
        books = Book.objects.filter(Q(title__icontains=search_book)|Q(author__icontains=search_book)).distinct()
        paginator = Paginator(books, 9)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        genre = Genre.objects.all().order_by('name')
        if not books:
            books = Book.objects.all()
            paginator = Paginator(books, 9)
            page = request.GET.get('page')
            books = paginator.get_page(page)
            error_message = "No Stories found try something else!"
            return render(request, 'index.html', {'error_message': error_message, 'books': books, 'genre':genre})
        return render(request,'index.html',{'books': books,'genre':genre })
    return render(request, 'index.html', context)

def categoryView(request, slug):
    genreC = get_object_or_404(Genre, slug=slug)
    category_post = Book.objects.filter(genre=genreC).order_by('title')
    genre = Genre.objects.all().order_by('name')
    paginator = Paginator(category_post, 10)
    page = request.GET.get('page')
    category_post = paginator.get_page(page)
    context = {'category_post':category_post, 'genre':genre, 'genreC':genreC}
    return render(request, 'category.html',context)



def bookDetail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    genre = Genre.objects.all().order_by('name')
    context = {'book': book, 'genre':genre}
    return render(request, 'book-detail.html', context)
    
@login_required
def submitRating(request, slug):
    if request.method == 'POST':
        rating_value = float(request.POST.get('rating'))
        book = get_object_or_404(Book, slug=slug)
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
    return redirect('book_detail', slug=slug)

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-date_added')
    genre = Genre.objects.all().order_by('name')
    if not cart_items:
        messages.error(request, 'Add at least one Story to your cart!')
        return redirect_to_previous_page(request)
    total_amount = 0
    for cart_item in cart_items:
        total_amount += cart_item.books.price * cart_item.quantity
    return render(request, 'shopping/cart.html', {'cart_items': cart_items, 'cart_total': total_amount, 'genre':genre})


@login_required
def add_to_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError()
    except (TypeError, ValueError):
        messages.error(request, 'Please enter a valid quantity.')
        return redirect_to_previous_page(request) 

    if book.quantity < 1:
        messages.error(request, 'Book Out of stock.')
        return redirect_to_previous_page(request)

    if book.quantity < quantity:
        messages.error(request, 'The requested quantity exceeds the available stock.')
        return redirect_to_previous_page(request)

    user = request.user
    existing_cart_item = Cart.objects.filter(user=user, books=book).first()
    
    if existing_cart_item:
        existing_cart_item.quantity += quantity
        existing_cart_item.save()
    else:
        cart_item = Cart(user=user, books=book, quantity=quantity)
        cart_item.save()

    book.quantity -= quantity
    book.save()
    
    messages.success(request, f'Added {quantity} {book.title} to the cart.')
    return redirect_to_previous_page(request)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, pk=item_id, user=request.user)

    if cart_item.user == request.user:
        cart_quantity = cart_item.quantity
        book = cart_item.books

        cart_item.delete()
        book.quantity += cart_quantity
        book.save()
        
        messages.success(request, 'Book removed from cart successfully.')
    
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, pk=item_id, user=request.user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        if new_quantity <= 0:
                messages.error(request, 'Please enter a valid quantity.')
        elif new_quantity > cart_item.books.quantity:
            messages.error(request, 'The requested quantity exceeds the available quantity.')
        else:
            change_in_quantity = new_quantity - cart_item.quantity
            cart_item.quantity = new_quantity
            cart_item.save()
            cart_item.books.quantity -= change_in_quantity
            cart_item.books.save()
            messages.success(request, 'Cart updated successfully.')
    
    return redirect('cart')

def calculateCartTotal(cart_items):
    total = 0
    for item in cart_items:
        total += item.books.price * item.quantity
    return total


@login_required
def checkoutView(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_amount = calculateCartTotal(cart_items)
    try:
        default_shipping_address = ShippingAddress.objects.get(customer=user, is_default=True)
    except ShippingAddress.DoesNotExist:
        default_shipping_address = None

    other_shipping_addresses = ShippingAddress.objects.filter(customer=user, is_default=False)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.customer = user
            shipping_address.save()

            ShippingAddress.objects.filter(customer=user).exclude(id=shipping_address.id).update(is_default=False)

            order = Order(user=user, total_amount=total_amount)
            order.save()
            order.items.set(cart_items)

            order_history = OrderHistory(
                user=user,
                items=order.items.all(),
                order_date=order.order_date,
                order_quantity=cart_items.count(),
                total_amount=order.total_amount,
                shipping_address=shipping_address
            )
            order_history.save()

            cart_items.delete()

            messages.success(request, 'Order placed successfully!')
            return redirect('order_history')
    else:
        form = ShippingAddressForm(instance=default_shipping_address)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'form': form,
        'shipping_address': default_shipping_address,
        'other_addresses': other_shipping_addresses,
    }

    return render(request, 'shopping/checkout.html', context)


@login_required
def add_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        try:
            if form.is_valid():
                shipping_address = form.save(commit=False)
                shipping_address.customer = request.user
                shipping_address.is_default = True 
                shipping_address.save()

                ShippingAddress.objects.filter(customer=request.user).exclude(id=shipping_address.id).update(is_default=False)

                messages.success(request, 'Shipping address added successfully.')
            else:
                messages.error(request, 'Invalid shipping address data. Please check your inputs.')
        except Exception as e:
            messages.error(request, 'An error occurred while adding the shipping address. Please try again later.')
        return redirect('checkout')  
    else:
        form = ShippingAddressForm()
    
    return render(request, 'shopping/add-address.html', {'form': form})

@login_required
def set_default_address(request, address_id):
    address = get_object_or_404(ShippingAddress, pk=address_id, customer=request.user)
    address.is_default = True
    address.save()
    ShippingAddress.objects.filter(customer=request.user).exclude(pk=address_id).update(is_default=False)
    messages.success(request, 'Default address set successfully.')
    return redirect('checkout')


@login_required
def order_history(request):
    user = request.user
    order_history = OrderHistory.objects.filter(user=user).order_by('-order_date')

    valid_order_history = []
    for order_entry in order_history:
        if order_entry.order.user == user:
            valid_order_history.append(order_entry)

    context = {'order_history': valid_order_history}
    return render(request, 'shopping/order-history.html', context)