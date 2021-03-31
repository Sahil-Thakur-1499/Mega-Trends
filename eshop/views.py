from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.
def home(request):
    products = Product.objects.all()
    categories=Category.objects.all()
    return render(request, 'eshop/home.html', {'products':products,'categories':categories})

def signup(request):
	categories=Category.objects.all()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.customer.name= form.cleaned_data.get('name')
			user.customer.phone= form.cleaned_data.get('phone')
			user.customer.email= form.cleaned_data.get('email')
			user.customer.address= form.cleaned_data.get('address')
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'eshop/signup.html', {'form': form,'categories':categories})

def category_detail(request,pk,flr):
	categories=Category.objects.all()
	ctg = get_object_or_404(Category, name=pk)
	if flr=='price_asc':
		products = Product.objects.filter(category=ctg.pk).order_by('price')
	elif flr=='price_desc':
		products = Product.objects.filter(category=ctg.pk).order_by('-price')
	elif flr=='rtg_asc':
		products = Product.objects.filter(category=ctg.pk).order_by('rating')
	elif flr=='rtg_desc':
		products = Product.objects.filter(category=ctg.pk).order_by('-rating')
	return render(request, 'eshop/category_detail.html', {'products':products,'categories':categories,'ctg':ctg,'flr':flr})

def contact_us(request):
    categories=Category.objects.all()
    return render(request, 'eshop/contact_us.html', {'categories':categories})

def product_detail(request,pk):
	categories=Category.objects.all()
	product = get_object_or_404(Product,id=pk)
	ctg = get_object_or_404(Category, name=product.category.name)
	r=range(product.rating+1,6)
	return render(request, 'eshop/product_detail.html', {'product':product,'categories':categories,'ctg':ctg,'r':r})