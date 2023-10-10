from django.http import HttpResponse
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
    search_book = request.GET.get('search')
    context = {'books': books, 'genre':genre}

    filter_form = BookFilterForm(request.GET)
    if filter_form.is_valid():
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')
        author = filter_form.cleaned_data.get('author')
        filters = Q()
        books = Book.objects.all().order_by('title')
        if min_price is not None:
            filters &= Q(price__gte=min_price)
        if max_price is not None:
            filters &= Q(price__lte=max_price)
        if author:
            filters &= Q(author__icontains=author)
        books = Book.objects.filter(filters).order_by('title')

    context = {'books': books, 'genre':genre, 'filter_form':filter_form}
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
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.save()
            return redirect('book_detail', slug=slug)

    else:
        comment_form = CommentForm()
        
    comments = Comment.objects.filter(book=book, active=True)
    context = {'book': book, 'genre':genre, 'comments':comments, 'comment_form':comment_form}
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
def add_comment(request, slug):
    book = get_object_or_404(Book, slug=slug)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = book
            new_comment.save()
            return redirect('book_detail', slug=slug)

    else:
        comment_form = CommentForm()
        
    comments = Comment.objects.filter(book=book, active=True)


    return redirect (request, 'book-detail.html', {'book':book,
                                           'comments':comments,
                                           'comment_form':comment_form})

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
## checkout process need a redesign
def checkoutView(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_amount = calculateCartTotal(cart_items)
    try:
        default_shipping_address = ShippingAddress.objects.get(user=user, is_default=True)
    except ShippingAddress.DoesNotExist:
        default_shipping_address = None

    other_shipping_addresses = ShippingAddress.objects.filter(user=user, is_default=False)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = user
            shipping_address.save()

            ShippingAddress.objects.filter(user=user).exclude(id=shipping_address.id).update(is_default=False)

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
## if want to add new address and change default
def add_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        try:
            if form.is_valid():
                shipping_address = form.save(commit=False)
                shipping_address.user = request.user
                shipping_address.is_default = True 
                shipping_address.save()

                ShippingAddress.objects.filter(user=request.user).exclude(id=shipping_address.id).update(is_default=False)

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
## done before the payment and placing order
def set_default_address(request, address_id):
    address = get_object_or_404(ShippingAddress, pk=address_id, user=request.user)
    address.is_default = True
    address.save()
    ShippingAddress.objects.filter(user=request.user).exclude(pk=address_id).update(is_default=False)
    messages.success(request, 'Default address set successfully.')
    return redirect('checkout')

@login_required
## should be done on the checkout page 
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user 
            order.save()
            return redirect('payment_gateway')
    else:
        form = OrderForm()

    return render(request, 'place_order.html', {'form': form})


@login_required
## after the payment is done
def order_history(request):
    user = request.user
    order_history = OrderHistory.objects.filter(user=user).order_by('-order_date')

    valid_order_history = []
    for order_entry in order_history:
        if order_entry.order.user == user:
            valid_order_history.append(order_entry)

    context = {'order_history': valid_order_history}
    return render(request, 'shopping/order-history.html', context)




    