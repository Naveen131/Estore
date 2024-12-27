from django.db import models

from accounts.models import User


# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    products = models.JSONField()  # {"product_id": quantity}
    total_price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id}"


class Toppings(models.Model):
    name = models.CharField(max_length=50, null=False,blank=False)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    STATUS_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
    ]
    toppings = models.ManyToManyField(Toppings, null=True, blank=True)
    name = models.CharField(max_length=50, null=False,blank=False)
    size = models.CharField(choices=STATUS_CHOICES, null=False,blank=False, max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class PizzaOrder(models.Model):
    pizzas = models.JSONField(null=False,blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
