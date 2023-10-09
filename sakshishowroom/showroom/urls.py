from django.contrib import admin
from django.urls import path,include, re_path
from . import views

urlpatterns = [
    path('', views.home, name='homepage' ),
    re_path('products', views.show_product),
    re_path('about', views.about),
    re_path('login', views.login, name="loginpage"),
    re_path('register', views.register),
    re_path('logout', views.LogOut),
    re_path('user/profile', views.UserProfile),
    re_path('cart/items', views.ShowCartItems),
    re_path('cart/set', views.AddToCart),
    re_path('cart/delete', views.RemoveFromCart),
    re_path('payment/verify', views.VerifyPayment),
    re_path('orders', views.OrdersListing),

]
