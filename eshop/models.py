from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=20)
	
	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=20)
	price = models.DecimalField(max_digits=7,decimal_places=2)
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	image = models.ImageField()
	description = models.TextField()
	rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	category = models.ForeignKey('eshop.Category', on_delete=models.CASCADE,related_name='Category')

	def __str__(self):
		return self.name

class User(models.Model):
	name = models.CharField(max_length=20)
	email = models.EmailField(max_length=255, unique=True)
	password = models.CharField(max_length=10)
	phone = models.DecimalField(max_digits=10,decimal_places=0,null=False, blank=False, unique=True)
	address = models.TextField()

	def __str__(self):
		return self.name

class Item(models.Model):
	product = models.ForeignKey('eshop.Product', on_delete=models.CASCADE,related_name='Product')
	qty = models.IntegerField()

	def price(self):
		return product.price*qty

class Cart(models.Model):
	user = models.ForeignKey('eshop.User', on_delete=models.CASCADE,related_name='User')
	items = models.ManyToManyField('eshop.Item', blank=True)
	amount = models.DecimalField(max_digits=7,decimal_places=2)

class Order(models.Model):
	ordered_date = models.DateTimeField(blank=True, null=True)
	pmntsts = models.BooleanField(default=False)
	cart = models.ForeignKey('eshop.Cart', on_delete=models.CASCADE,related_name='Cart')
