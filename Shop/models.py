from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShopDetail(models.Model):
    usr = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Shopname = models.TextField(max_length=30, null=True)
    Shop_Image = models.FileField(null=True)
    Phone = models.TextField(max_length=10,null=True)

    def __str__(self):
        return self.usr.username+'--'+self.Shopname

class Item(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(ShopDetail, on_delete=models.CASCADE, null=True)
    Product_name = models.TextField(max_length=20, null=True)
    Price = models.FloatField(blank=True, null=True)
    Quantity = models.TextField(max_length=4, null=True)
    Product_Type = models.TextField(max_length=20, null=True)
    Product_Image = models.FileField(null=True)
    Product_Dis = models.TextField(max_length=50, null=True)

    def __str__(self):
        return self.usr.username+'--'+self.Product_name


class Like(models.Model):
    post_data = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    usr = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    like = models.BooleanField(default=False)


    def __str__(self):
        return self.Item.Product_name