"""Green_Graderning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Main import views as mv
from Shop import views as sv

urlpatterns = [
    path('admin/', admin.site.urls),

    #Main.urls
    path('', mv.Index, name='Index'),
    path('shop/', mv.Shop, name='Shop'),
    path('product/<int:pid>', mv.Product_Detail, name='PDetail'),
    path('cart/', mv.Cart, name='Cart'),
    path('add-to-cart/<int:pid>', mv.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pid>', mv.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<int:pid>', mv.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('checkout/', mv.Checkout, name='Checkout'),
    path('order-placed/', mv.Confirm, name='Confirm'),
    path('contact/', mv.Contact, name='Contact'),
    path('login/', mv.Login, name='Login'),
    path('signup/', mv.Singup, name='Signup'),
    path('logout/', mv.Logout, name='Logout'),


    #Shop.urls
    path('shop/my', sv.Shop, name='YourShop'),
    path('shop/login/', sv.Login, name='SLogin'),
    path('shop/signup/', sv.Singup, name='SSignup'),
    path('shop/logout/', sv.Logout, name='SLogout'),
    path('shop/itemdelete/<int:pid>', sv.product_delete, name='productdelete'),
    path('shop/Orders/', sv.Order_Dasboard, name='SOrder'),
    path('shop/edit-product/<int:pid>', sv.Product_Edit, name='PEdit'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
