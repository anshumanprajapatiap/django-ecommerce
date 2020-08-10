from django.db import models
from django.contrib.auth.models import User
from Shop.models import Item


# Create your models here.

class UserDetail(models.Model):
    usr = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Phone = models.TextField(max_length=10, null=True)

    def __str__(self):
        return self.usr.username



class OrderItem(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.Product_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.Price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    street_address = models.CharField(max_length=100, null=True)
    apartment_address = models.CharField(max_length=100, null=True)
    country = models.TextField(max_length=100, null=True)
    zip = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.usr.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class Address(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    street_address = models.CharField(max_length=100, null=True)
    apartment_address = models.CharField(max_length=100, null=True)
    country = models.TextField(max_length=100, null=True)
    zip = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.usr.username




