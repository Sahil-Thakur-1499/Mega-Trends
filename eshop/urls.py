from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup',views.signup,name='signup'),
	path('category/<str:pk>', views.category_detail, name='category_detail'),
	path('contact-us',views.contact_us,name='contact_us'),
]
