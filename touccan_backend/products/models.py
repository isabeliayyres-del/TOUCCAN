from django.db import models
from merchants.models import Merchant


class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        return self.cat_name
    
    class Meta:
        db_table = 'categories' 


class Product(models.Model):
    name = models.CharField(max_length=200)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'products' 
