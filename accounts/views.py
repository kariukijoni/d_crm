from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

from .forms import OrderForm
# Create your views here.


def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()



    total_customers=customers.count()
    total_orders=orders.count()

    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context= {'customers':customers,'orders':orders,'total_customers':total_customers,'total_orders':total_orders,
              'delivered':delivered,'pending':pending }
    

    return render(request, 'accounts/dashboard.html',context)

def products(request):
    products=Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})


def customers(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    order_count=orders.count()
    context= {'customer':customer,'orders':orders,'order_count':order_count}

    return render(request, 'accounts/customers.html',context)

def createOrder(request):
        
        form=OrderForm()

        if request.method == 'POST':
            #  print('printing data',request.POST)
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save()

                return redirect('/home')
    
        context={'form':form}
        return render (request,'accounts/order_form.html',context)
    


