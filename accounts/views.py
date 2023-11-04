from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

from .decorators import unauthenticated_user,allowed_users,admin_only

from django.contrib.auth.models import Group 

from .filters import OrderFilter
# Create your views here.

@unauthenticated_user
def loginPage(request):

        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            
            else:
                messages.info(request,'Username or Password is incorect')
                # return render(request,'accounts/user/login.html',context)

        context = {}

        return render(request, 'accounts/user/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):
    
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                
                username=form.cleaned_data.get('username')

                # Associate register user to a group
                group=Group.objects.get(name='customer')
                user.groups.add(group)

                messages.success(request,'Account was created for '+ username)
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/user/register.html', context)


def userPage(request):

    context = {}
    return render(request, 'accounts/user.html', context)




@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin','customer'])
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers': customers, 'orders': orders, 'total_customers': total_customers, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    context = {'customer': customer, 'orders': orders,
               'order_count': order_count, 'order_filter': order_filter}

    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    # populate field customer
    # form=OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        #  print('printing data',request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()

            return redirect('/')

    # context={'form':form}
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()

        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete_form.html', context)
