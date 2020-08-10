from django.shortcuts import render, redirect
from .models import *
from Shop.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def Index(request):
    customer_data = UserDetail.objects.all()
    shop_data = ShopDetail.objects.all()
    Product_data = Item.objects.all()
    recent4 = recent()
    d = {'customer_data': customer_data, 'shop_data': shop_data, 'product_data': Product_data, 'recent4': recent4}
    return render(request, 'index.html', d)

def Login(request):
    error = False
    shop = False
    if request.method == 'POST':
        x = request.POST
        us = x['usr']
        pa = x['pas']
        user = authenticate(username=us, password=pa)

        if user:
            for i in UserDetail.objects.all():
                if str(i.usr) == us:
                    login(request, user)
                    return redirect('Shop')
                else:
                    shop = True
        else:
            error = True
    d = {"error": error, "Shop": shop}
    return render(request, 'login.html', d)

def Singup(request):
    error = False
    password_error = False
    if request.method == 'POST':
        dd = request.POST
        f = dd['first']
        l = dd['last']
        u = dd['em']
        e = dd['em']
        p = dd['pwd']
        p2 = dd['pwd2']
        phone = dd['phone']
        if p != p2:
            password_error = True
        else:
            udata = User.objects.filter(username=u)
            if udata:
                error = True
            else:
                user = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
                UserDetail.objects.create(usr=user, Phone=phone)
                return redirect('Login')
    d = {"error": error, "password_error": password_error}
    return render(request, 'signup.html', d)

def Logout(request):
    logout(request)
    return redirect('Login')

def Shop(request):
    customer_data = UserDetail.objects.all()
    shop_data = ShopDetail.objects.all()
    Product_data = Item.objects.all()
    d = {'customer_data': customer_data, 'shop_data': shop_data, 'product_data': Product_data}
    return render(request, 'shop.html', d)

def Product_Detail(request, pid):
    detail = Item.objects.get(id=pid)
    d = {'detail': detail}
    return render(request, 'shop-details.html', d)

def recent():
    allpost = Item.objects.all()
    recent_four = allpost[::-1][:4]
    return recent_four

def Cart(request):
    try:
        order = Order.objects.get(usr=request.user, ordered=False)
        d = {'object': order}
        return render(request, 'cart.html', d)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect('Shop')


def add_to_cart(request, pid):
    item = Item.objects.get(id=pid)
    order_item, created = OrderItem.objects.get_or_create(item=item, usr=request.user, ordered=False)
    order_qs = Order.objects.filter(usr=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("Cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("Cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(usr=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("Cart")


def remove_from_cart(request, pid):
    item = Item.objects.get(id=pid)
    order_qs = Order.objects.filter(usr=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(item=item, usr=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("Cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("Cart")

def remove_single_item_from_cart(request, pid):
    item = Item.objects.get(id=pid)
    order_qs = Order.objects.filter(usr=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(item=item, usr=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("Cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Cart")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("Cart")


def Checkout(request):
    try:
        if request.method == 'POST':
            dd = request.POST
            s = dd['sa']
            a = dd['apart']
            c = dd['cunt']
            z = dd['zip']

            adata = Address.objects.filter(usr=request.user)
            print(adata)
            if adata:
                Address.objects.update(usr=request.user, street_address=s, apartment_address=a, country=c, zip=z)
            else:
                Address.objects.create(usr=request.user, street_address=s, apartment_address=a, country=c, zip=z)

            Order.objects.update(usr=request.user, ordered=True, street_address=s, apartment_address=a, country=c, zip=z)
            return redirect('Confirm')
        order = Order.objects.get(usr=request.user, ordered=False)
        d = {'object': order}
        return render(request, 'checkout.html', d)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect('Shop')

def Confirm(request):
    return render(request, 'confirmation.html')

def Contact(request):
    return render(request, 'contact.html')

