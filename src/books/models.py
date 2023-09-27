from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

    
# form publishing/adding new book
status = (
    (0, "Draft"),
    (1, "Publish")
)
class Book(models.Model):
    title  		 = models.CharField(max_length=200)
    author 		 = models.CharField(max_length=100)
    genre   	 = models.CharField(max_length=100)
    price  		 = models.FloatField(default=0)
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


# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)
    
#     def __str__(self):
#         return self.name
    

class CustomerRating(models.Model):
    user   	= models.ForeignKey(User,on_delete=models.CASCADE) 
    book 	= models.ForeignKey(Book,on_delete=models.CASCADE)
    rating 	= models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])

    def __str__(self):
        return f"{self.user.username} - {self.book.title}: {self.rating}"
    

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    books = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)