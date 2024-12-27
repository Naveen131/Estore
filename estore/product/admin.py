from django.contrib import admin

from product.models import Product, Order

from product.models import Pizza, PizzaOrder

from product.models import Toppings

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Toppings)
admin.site.register(Pizza)
admin.site.register(PizzaOrder)
