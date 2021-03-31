from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True)
    phone=models.CharField(max_length=10,null=True)
    email=models.EmailField(null=True)
    address=models.TextField(null=True)
    
    def __str__(self):
        return self.user.username        
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)
        instance.customer.save()

class Item(models.Model):
	product = models.ForeignKey('eshop.Product', on_delete=models.CASCADE,related_name='Product')
	qty = models.IntegerField(default=1)
	
	def price(self):
		return self.product.price*self.qty
	def __str__(self):
			return self.product.name

class Cart(models.Model):
	customer=models.ForeignKey('eshop.Customer', on_delete=models.CASCADE,related_name='Customer')
	# items = models.ForeignKey('eshop.Item',on_delete=models.CASCADE,related_name='Item')
	items=models.ManyToManyField('eshop.Item')
	amount = models.DecimalField(max_digits=7,decimal_places=2)
	def __str__(self):
			return self.customer.name

class Order(models.Model):
	ordered_date = models.DateTimeField(blank=True, null=True)
	pmntsts = models.BooleanField(default=False)
	cart = models.ForeignKey('eshop.Cart', on_delete=models.CASCADE,related_name='Cart')
