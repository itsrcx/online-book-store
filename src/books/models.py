from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


# form publishing/adding new book
status = (
    (0, "Draft"),
    (1, "Publish")
)
class Books(models.Model):
	title           = models.CharField(max_length=200)
    author          = model.CharField(max_length=100)
	category        = models.CharField(max_length=100)
    price           = models.FloatField()
    quantity        = models.IntegerField()
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField(auto_now=True) 
	book_thumbnail  = models.FileField()
    status          = models.IntegerField(choices=status,default = 1)
    
    class Meta:
        ordering    = ['quantity']

	def __str__(self):
		return self.name 


class Customer(models.Model):
    None 

class CustomerRating(models.Model):
	user   	= models.ForeignKey(User,on_delete=models.CASCADE) 
	book 	= models.ForeignKey(Books,on_delete=models.CASCADE)
	rating 	= models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])