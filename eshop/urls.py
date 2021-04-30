from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('signup',views.signup,name='signup'),
    path('category/<str:pk>?sortby=<str:flr>', views.category_detail, name='category_detail'),
    path('contact-us',views.contact_us,name='contact_us'),
    path('login/', auth_views.LoginView.as_view(template_name='eshop/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('product-detail/<str:pk>', views.product_detail,name="product_detail"),
    path('add_to_cart/<str:pk>',views.atc,name="atc"),
    path('mycart/',views.v_cart,name="v_cart"),
    path('mycart/del/<str:pk>',views.delitem,name="delitem"),
    path('mycart/plus/<str:pk>',views.plus,name="plus"),
    path('mycart/minus/<str:pk>',views.minus,name="minus"),
    path('checkout/<str:pk>',views.checkout,name="checkout"),
    
]
