from django.db import models
from django.utils import timezone
from users.models import User
from products.models import Product
from orders.models import Order

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"Cart {self.id} (user={self.user_id})"

    def total(self):
        qs = self.items.select_related('product').all()
        total = sum(item.product.price * item.quantity for item in qs if item.product and item.product.price)
        return total

class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product_id} in cart {self.cart_id}"

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50, default='dummy')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # pending, paid, failed
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"Payment {self.id} for order {self.order_id} ({self.status})"
