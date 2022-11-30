from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
AbstractUser._meta.get_field('email')._unique = True

USER_OPTIONS = (
    ('user', 'user'),
    ('admin', 'admin'),
    ('super-admin', 'super-admin')
)

class SiteUser(AbstractUser):
    shipping_address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    special_user = models.CharField(max_length=20, choices=USER_OPTIONS, default='user')
    
    class Meta:
        unique_together = ('username', 'email')