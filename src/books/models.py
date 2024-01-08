from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

    
# form publishing/adding new book

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    def __str__(self):
        return self.name

 
class Book(models.Model):
    status_choice = (
    (0, "Draft"),
    (1, "Publish")
    )
    title  		 = models.CharField(max_length=200)
    slug         = models.SlugField(max_length=140, unique=True)
    author 		 = models.CharField(max_length=100)
    genre        = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)    
    price     	 = models.FloatField(default=0)
    quantity   	 = models.PositiveIntegerField()
    description  = models.TextField(default='No Description', null=True, blank=False)
    average_rating  = models.FloatField(default=0)
    created_on 	 = models.DateTimeField(auto_now_add=True)
    updated_on 	 = models.DateTimeField(auto_now=True)
    # book_thumbnail  = models.FileField()
    digital         = models.BooleanField(default=False, null=True, blank=False)
    status          = models.IntegerField(choices=status_choice,default = 1)
    
    class Meta:
        ordering    = ['-quantity']

    def __str__(self):
        return self.title
    
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Book.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    books = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s cart item: {self.book.title}"
        

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = (
    ('cash_on_delivery', 'Cash on Delivery'),
    ('card_payment', 'Card Payment'),
    ('upi_payment', 'UPI Payment'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    items = models.ManyToManyField(Book)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_complete = models.BooleanField(default=False, null=True, blank=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True) 
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)    
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.address)
    
class Checkout(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, unique=True)
    payment_status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"Checkout for Order {self.order.id}"

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    order_date = models.DateTimeField(auto_now_add=True)
    order_quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} and Amount {self.total_amount}"

 
class CustomerRating(models.Model):
    user   	= models.ForeignKey(User, on_delete=models.CASCADE)
    book 	= models.ForeignKey(Book, on_delete=models.CASCADE)
    rating 	= models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}: {self.rating}"

    
class Comment(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body,self.name)