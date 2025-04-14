# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    place = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)  # Ensure unique emails

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50)  # e.g., Breakfast, Lunch
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class SideDish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='side_dishes')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} for {self.menu.name}"

class Stock(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='stock')
    available_stock = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.menu.name}: {self.available_stock} units"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    token_number = models.CharField(max_length=10, unique=True, default=uuid.uuid4().hex[:6])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.token_number} by {self.student.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu.name} for Order {self.order.token_number}"

class OrderSideDish(models.Model):
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, related_name='side_dishes')
    side_dish = models.ForeignKey(SideDish, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.side_dish.name} for Order {self.order_detail.order.token_number}"

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('resolved', 'Resolved'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    description = models.TextField()
    reply = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.student.username} ({self.status})"

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.token_number}: {self.status}"
    
    

# core/models.py (add at bottom)
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Stock)
def stock_alert(sender, instance, **kwargs):
    if instance.available_stock < 10:
        # Simulate alert (e.g., email to admin)
        print(f"Low stock alert: {instance.menu.name} has {instance.available_stock} units")


# core/models.py (add below stock_alert)
@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    if created:
        # Simulate email notification
        print(f"Order {instance.token_number} placed by {instance.student.username}")