from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home,name='home'),
    path('products/', views.products,name='products'),
    path('customers/', views.customers,name='customers'),
    path('dashboard/',views.dashboard,name='dashboard')
]
