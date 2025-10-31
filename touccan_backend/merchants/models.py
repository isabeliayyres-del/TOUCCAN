from django.db import models
from users.models import User


class Merchant(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_merchants')
    merchant_name = models.CharField(max_length=150)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.merchant_name
    
    class Meta:
        db_table = 'merchants' 
