from django.db import models
import random
import re
from PIL import Image
from io import BytesIO
from django.core.files import File







class Shop(models.Model):
    shop_owner = models.CharField(max_length=255, default='null')
    shopname = models.CharField(max_length=255, default='null')
    location = models.CharField(max_length=255, default='null')
    phone_no = models.CharField(max_length=255, default='null')
    email = models.CharField(max_length=255, default='null')

    def __str__(self):
        return f'Shop {self.id}: {self.shopname}: {self.location} : {self.shop_owner} : {self.email}'


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    
    title = models.CharField(max_length=100)
    
    description = models.TextField()
    location = models.CharField(max_length=100, default='null')
    quantity = models.IntegerField(default=0)
    returned = models.IntegerField(default=0)
    

    
    category = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        if self.shop:
            self.location = self.shop.location  # Assign the location from the associated shop
       
            

            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @classmethod
    def create_product_with_shop(cls, shop_id, **kwargs):
        try:
            shop = Shop.objects.get(pk=shop_id)
        except Shop.DoesNotExist:
            raise ValueError(f"Shop with ID {shop_id} does not exist.")

        product = cls(shop=shop, **kwargs)
        product.save()
        return product

    