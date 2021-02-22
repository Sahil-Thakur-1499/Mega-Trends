from django.shortcuts import render,redirect,get_object_or_404
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

def category_detail(request,pk):
	categories=Category.objects.all()
	ctg = get_object_or_404(Category, name=pk)
	products = Product.objects.filter(category=ctg.pk)
	return render(request, 'eshop/category_detail.html', {'products':products,'categories':categories,'ctg':ctg})

def contact_us(request):
    categories=Category.objects.all()
    return render(request, 'eshop/contact_us.html', {'categories':categories})
