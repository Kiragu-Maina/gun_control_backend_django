from django.contrib import admin
from .models import Product, Shop, Medication, Cart, CartItem

admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Medication)
admin.site.register(Cart)
admin.site.register(CartItem)

# Register your models here.
