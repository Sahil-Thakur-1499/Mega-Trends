from django.shortcuts import render,redirect
from .models import *
from .forms import SignUpForm

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
			user = form.save(commit=False)
			user.save()
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'eshop/signup.html', {'form': form,'categories':categories})