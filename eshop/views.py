from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
import datetime
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.http import HttpResponse
from django.shortcuts import render
from mysite.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import get_template
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def home(request):
	products = Product.objects.all()
	categories=Category.objects.all()
	c=0
	cart=None
	if request.user.is_authenticated:
		customer=get_object_or_404(Customer,user=request.user)
		cart=Cart.objects.filter(customer=customer)
		if cart.exists():
			c=1
			cart = cart[0]
	return render(request, 'eshop/home.html', {'products':products,'categories':categories,'c':c,'cart':cart})

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
			subject = 'Welcome to Mega Trends'
			message = 'Welcome to Online MegaStore:MegaTrends'+'\n'+'Your Username is: '+str(user.customer.name)
			recepient = user.customer.email
			send_mail(subject,message, EMAIL_HOST_USER, [recepient], fail_silently = False)
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
@login_required(login_url='login')
def atc(request,pk):
	categories=Category.objects.all()
	product = get_object_or_404(Product,id=pk)
	customer=get_object_or_404(Customer,user=request.user)
	item, created = Item.objects.get_or_create(product=product,customer=customer)
	cart=Cart.objects.filter(customer=customer)
	if cart.exists():
		cart = cart[0]
		product.quantity=product.quantity-1
		product.save()
		if cart.items.filter(product=product).exists():
			item.qty += 1
			item.save()
			cart.amount+=item.price()/item.qty
			cart.save()
			messages.info(request, "Item qty was updated.")
			return redirect("/mycart",{'categories':categories})
		else:
			cart.items.add(item)
			cart.amount+=item.price()
			cart.save()
			messages.info(request, "Item was added to your cart.")
			return redirect("/mycart",{'categories':categories})
	else:
		cart=Cart()
		cart.customer=customer
		cart.amount=item.price()
		cart.save()
		cart.items.add(item)
		cart.save()
		product.quantity=product.quantity-1
		product.save()
		messages.info(request, "Item was added to your cart.")
		return redirect("/mycart",{'categories':categories})

@login_required(login_url='login')
def v_cart(request):
	categories=Category.objects.all()
	customer=get_object_or_404(Customer,user=request.user)
	cart=Cart.objects.filter(customer=customer)
	c=0
	if cart.exists():
		c=1
		cart = cart[0]
	return render(request,"eshop/mycart.html",{'categories':categories,'c':c,'cart':cart})

def delitem(request,pk):
	categories=Category.objects.all()
	customer=get_object_or_404(Customer,user=request.user)
	cart=Cart.objects.filter(customer=customer)
	c=0
	if cart.exists():
		c=1
		cart = cart[0]
	item = get_object_or_404(Item,id=pk)
	product = get_object_or_404(Product,id=item.product.pk)
	product.quantity+=item.qty
	product.save()
	cart.amount-=item.price()
	item.delete()
	cart.save()
	if cart.items.all().count()==0:
		cart.delete()
		c=0
	return redirect("/mycart/",{'categories':categories,'c':c,'cart':cart})

def plus(request,pk):
	categories=Category.objects.all()
	customer=get_object_or_404(Customer,user=request.user)
	cart=Cart.objects.filter(customer=customer)
	c=0
	if cart.exists():
		c=1
		cart = cart[0]
	item = get_object_or_404(Item,id=pk)
	product = get_object_or_404(Product,id=item.product.pk)
	if product.quantity>0:
		item.qty+=1
		item.save()
		product.quantity-=1
		product.save()
		cart.amount+=item.price()/item.qty
		cart.save()
	return redirect("/mycart/",{'categories':categories,'c':c,'cart':cart})

def minus(request,pk):
	categories=Category.objects.all()
	customer=get_object_or_404(Customer,user=request.user)
	cart=Cart.objects.filter(customer=customer)
	c=0
	if cart.exists():
		c=1
		cart = cart[0]
	item = get_object_or_404(Item,id=pk)
	product = get_object_or_404(Product,id=item.product.pk)
	cart.amount-=item.price()/item.qty
	cart.save()
	item.qty-=1
	item.save()
	product.quantity+=1
	product.save()
	if item.qty==0:
		item.delete()
		if cart.items.all().count()==0:
			cart.delete()
			c=0
	return redirect("/mycart/",{'categories':categories,'c':c,'cart':cart})

def checkout(request,pk):
	categories=Category.objects.all()
	cart=get_object_or_404(Cart,id=pk)
	order=Order.objects.filter(cart=cart)
	if order.exists():
		order = order[0]
	else:
		order=Order()
		order.pmntsts=False
		order.ordered_date=datetime.datetime.now()	
		order.cart=cart
		order.save()
	return render(request,"eshop/checkout.html",{'categories':categories,'order':order})

def payment(request,pk):
	order=get_object_or_404(Order,id=pk)
	amount = float(order.cart.amount*100)
	client = razorpay.Client(auth=(os.environ.get('KEY'),os.environ.get('SECRET')))
	response = client.order.create({'amount':amount,'currency':'INR','payment_capture':1})
	print(response)
	context = {'response':response,'order':order}
	return render(request,"eshop/razorpay.html",context)


@csrf_exempt
def payment_success(request,pk):
    if request.method =="POST":
    	order=get_object_or_404(Order,id=pk)
    	po=Placed_Order()
    	subject = 'Your Order Has Been Placed Successfully!!'
    	recepient = order.cart.customer.email
    	html=render_to_string('eshop/success2.html', {'order': order})
    	text_content = strip_tags(html)
    	email = EmailMultiAlternatives(subject,text_content, from_email=EMAIL_HOST_USER, to=[recepient])
    	email.attach_alternative(html, "text/html")
    	email.encoding = 'us-ascii'
    	email.send()
    	po.i=order.pk
    	po.ordered_date=datetime.datetime.now()
    	po.customer=order.cart.customer
    	po.amount=order.cart.amount
    	po.status="Paid and Under Process"
    	cart=get_object_or_404(Cart,id=order.cart.pk)
    	po.items=""
    	for item in cart.items.all():
    		po.items+=str(item.product.name)+'-'+str(item.qty)+'\n'
    		item.delete()
    	po.save()
    	cart.delete()
    	print(request.POST)
    	return render(request, 'eshop/success.html', {'order': order})

def profile(request):
	categories=Category.objects.all()
	if request.user.is_authenticated:
		customer=get_object_or_404(Customer,user=request.user)
		po=Placed_Order.objects.filter(customer=customer)
		if request.method == "POST":
			form = UpdateForm(data=request.POST,instance=customer)
			if form.is_valid():
				user = form.save()
				categories=Category.objects.all()
				po=Placed_Order.objects.filter(customer=customer)
				return render(request, 'eshop/profile.html', {'customer':customer,'categories':categories,'po':po,'form':form})	
		else:
			form = UpdateForm(instance=customer)
			return render(request, 'eshop/profile.html', {'customer':customer,'categories':categories,'po':po,'form': form})    
	return render(request, 'eshop/profile.html', {'customer':customer,'categories':categories,'po':po})		
