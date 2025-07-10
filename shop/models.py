from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Artisan(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artisan_profile', null=True, blank=True)
    name        = models.CharField(max_length=150)
    email       = models.EmailField(max_length=254)
    phone       = models.CharField(max_length=20)
    biography   = models.TextField()
    region      = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='artisans')
    main_image  = models.ImageField(upload_to='artisans/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name                  = models.CharField(max_length=200)
    description           = models.TextField()
    materials             = models.CharField(max_length=200)
    dimensions            = models.CharField(max_length=100)
    cultural_significance = models.TextField(blank=True)
    category              = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    region                = models.ForeignKey(Region,   on_delete=models.CASCADE, related_name='products')
    artisan               = models.ForeignKey(Artisan,  on_delete=models.SET_NULL, null=True, related_name='products')
    main_image            = models.ImageField(upload_to='products/', null=True, blank=True)
    price                 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name         = models.CharField(max_length=150)
    email        = models.EmailField()
    message      = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message from {self.name} at {self.submitted_at}"