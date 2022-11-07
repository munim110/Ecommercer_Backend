from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
AbstractUser._meta.get_field('email')._unique = True

class SiteUser(AbstractUser):
    shipping_address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    special_user = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('username', 'email')