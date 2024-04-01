from django.contrib import admin
from .models import Product, Shop, Medication, Cart, CartItem, Order

admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Medication)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)

# Register your models here.
