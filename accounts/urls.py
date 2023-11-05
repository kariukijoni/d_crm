from django.contrib import admin
from django.urls import path
from . import views

from django.contrib.auth.views import(PasswordResetView,PasswordResetConfirmView,
PasswordResetDoneView,PasswordResetCompleteView)

urlpatterns = [
    path('', views.home,name='home'),

    path('login/', views.loginPage,name='login'),
    path('register/', views.registerPage,name='register'),
    path('logout/',views.logoutUser,name='logout'),

    path('user/',views.userPage,name='user_page'),

    path('account/',views.accountSettings,name='account'),

    path('products/', views.products,name='products'),
    path('customer/<str:pk>/', views.customers,name='customer'),
    path('create_order/<str:pk>/', views.createOrder,name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder,name='delete_order'),

    path('password-reset/', 
        PasswordResetView.as_view(template_name='accounts/user/password_reset.html'),
        name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='accounts/user/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-done/',
        PasswordResetDoneView.as_view(template_name='accounts/user/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset-complete/',
        PasswordResetCompleteView.as_view(template_name='accounts/user/password_reset_complete.html'),
        name='password_reset_complete'),
]
