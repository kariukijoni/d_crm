from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

from .forms import OrderForm
from django.forms import inlineformset_factory

from .filters import OrderFilter
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

    order_filter=OrderFilter(request.GET,queryset=orders)
    orders=order_filter.qs

    context= {'customer':customer,'orders':orders,'order_count':order_count,'order_filter':order_filter}

    return render(request, 'accounts/customers.html',context)

def createOrder(request,pk):
        OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)

        customer=Customer.objects.get(id=pk)
        formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)


        # populate field customer
        # form=OrderForm(initial={'customer':customer})


        if request.method == 'POST':
            #  print('printing data',request.POST)
            formset = OrderFormSet    (request.POST,instance=customer)
            if formset.is_valid():
                formset.save()

                return redirect('/')
    
        # context={'form':form}
        context={'formset':formset}
        return render (request,'accounts/order_form.html',context)
    


def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form =OrderForm(instance=order)


    
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()

            return redirect('/')

    context={'form':form}
    return render (request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)

    if request.method=='POST':
        order.delete()

        return redirect('/')

    context={'item':order}
    return render (request,'accounts/delete_form.html',context)