from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=20)
	price = models.DecimalField(max_digits=7,decimal_places=2)
	quantity = models.IntegerField(validators=[MinValueValidator(0)])
	image = models.ImageField(upload_to=None)
	description = models.TextField()
	rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	def __str__(self):
		return self.name