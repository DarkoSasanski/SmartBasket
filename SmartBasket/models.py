from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Market(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Salesman(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Deliveryman(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} во {self.market}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    def __str__(self):
        return f'Кошничката на {self.customer}\' во маркетот {self.market}'


class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.shopping_cart} - {self.product}'


class PickUpOrder(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_pickup = models.DateTimeField()
    phone_number = models.CharField(max_length=100)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    picked_up = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Нарачка за подигнување на {self.first_name} {self.last_name}'


class DeliveryOrder(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    PAYMENT_CHOICES = (
        ('door', 'Наплата при достава'),
        ('online', 'Наплата со картичка'),
    )
    payment_option = models.CharField(max_length=30, choices=PAYMENT_CHOICES)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    deliveryman = models.ForeignKey(Deliveryman, on_delete=models.CASCADE, null=True, blank=True)
    delivered = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Нарачка за достава на {self.first_name} {self.last_name}'


class PickUpOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(PickUpOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product} - {self.quantity}'


class DeliveryOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product} - {self.quantity}'
