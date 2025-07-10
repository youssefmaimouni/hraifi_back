from django.contrib import admin
from .models import Category, Region, Artisan, Product, ContactMessage

# Register your shop models
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(Artisan)
admin.site.register(Product)
admin.site.register(ContactMessage)