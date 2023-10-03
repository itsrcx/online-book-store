from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

    
# form publishing/adding new book
status = (
    (0, "Draft"),
    (1, "Publish")
)
class Book(models.Model):
    title  		 = models.CharField(max_length=200)
    slug         = models.SlugField(max_length=140, unique=True)
    author 		 = models.CharField(max_length=100)
    genre   	 = models.CharField(max_length=100)
    price     	 = models.FloatField(default=0)
    quantity   	 = models.IntegerField(default=0)
    description  = models.TextField(default='No Description', null=True, blank=False)
    average_rating  = models.FloatField(default=0)
    created_on 	 = models.DateTimeField(auto_now_add=True)
    updated_on 	 = models.DateTimeField(auto_now=True)
    # book_thumbnail  = models.FileField()
    digital         = models.BooleanField(default=False, null=True, blank=False)
    status          = models.IntegerField(choices=status,default = 1)
    
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
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s cart item: {self.book.title}"
        

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    items = models.ManyToManyField(Cart)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    complete = models.BooleanField(default=False, null=True, blank=False)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
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
    user   	= models.ForeignKey(User,on_delete=models.CASCADE) 
    book 	= models.ForeignKey(Book,on_delete=models.CASCADE)
    rating 	= models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])

    def __str__(self):
        return f"{self.user.username} - {self.book.title}: {self.rating}"