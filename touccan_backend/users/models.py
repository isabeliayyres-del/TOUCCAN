from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('merchant', 'Merchant'),
    ]

    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # country = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'     
    
