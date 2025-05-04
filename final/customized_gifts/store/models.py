from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    quantity_in_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    # For logged-in users
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # For guest users
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)

    # Common fields
    customer_address = models.TextField(null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user or self.guest_email or self.guest_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customization = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order #{self.order.id}"


class GuestCart(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    cart_data = models.JSONField()
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.email} saved at {self.saved_at}"
