from django.shortcuts import render, redirect
from .models import *
from Main.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def Shop(request):
    customer_data = UserDetail.objects.all()
    shop_data = ShopDetail.objects.all()
    Product_data = Item.objects.all()
    if request.method == 'POST':
        dd = request.POST
        n = dd['name']
        p = dd['price']
        q = dd['quantity']
        t = dd['type']
        img = request.FILES['pimage']
        d = dd['name']
        user = request.user
        for i in shop_data:
            if i.usr.username == request.user.username:
                shop_name = i

        Item.objects.create(usr=user, shop=shop_name, Product_name=n, Price=p, Quantity=q, Product_Type=t, Product_Dis=d, Product_Image=img)
        return redirect('YourShop')
    d = {'customer_data': customer_data, 'shop_data': shop_data, 'product_data': Product_data}
    return render(request, 'yourshop.html', d)

def Login(request):
    error = False
    cust = False
    if request.method == 'POST':
        x = request.POST
        us = x['shopusr']
        pa = x['shoppas']
        user = authenticate(username=us, password=pa)

        if user:
            for i in ShopDetail.objects.all():
                if str(i.usr) == us:
                    login(request, user)
                    return redirect('YourShop')
                else:
                    cust = True
        else:
            error = True
    d = {"error": error, "cust": cust}
    return render(request, 'slogin.html', d)


def Singup(request):
    error = False
    password_error = False
    if request.method == 'POST':
        dd = request.POST
        sh = dd['shop_name']
        f = dd['first']
        l = dd['last']
        e = dd['email']
        p = dd['pwd']
        p2 = dd['pwd2']
        phone = dd['phone']
        shimg = request.FILES['shop_image']
        if p != p2:
            password_error = True
        else:
            udata = User.objects.filter(username=e)
            if udata:
                error = True
            else:
                user = User.objects.create_user(username=e, password=p, email=e, first_name=f, last_name=l)
                ShopDetail.objects.create(usr=user, Phone=phone, Shopname=sh, Shop_Image=shimg)
                return redirect('SLogin')
    d = {"error": error, "password_error": password_error}
    return render(request, 'ssignup.html', d)


def Logout(request):
    logout(request)
    return redirect('SLogin')


def product_delete(request,pid):
    data = Item.objects.get(id=pid)
    data.delete()
    return redirect('YourShop')

def Product_Edit(request,pid):
    detail = Item.objects.get(id=pid)
    if request.method == 'POST':
        dd = request.POST
        n = dd['name']
        p = dd['price']
        q = dd['quantity']
        t = dd['type']
        img = request.FILES['pimage']
        d = dd['name']
        user = request.user
        for i in shop_data:
            if i.usr.username == request.user.username:
                shop_name = i

        Item.objects.update(usr=user, shop=shop_name, Product_name=n, Price=p, Quantity=q, Product_Type=t, Product_Dis=d, Product_Image=img)
        return redirect('YourShop')
    d = {'detail': detail}
    return render(request, 'edit-p.html', d)


def Order_Dasboard(request):
    try:
        order = Order.objects.all()
        orderitems = OrderItem.objects.all()
        print(orderitems)
        d = {'object': order, 'objects': orderitems}
        return render(request, 'order_dasboard.html', d)
    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        return redirect('YourShop')

