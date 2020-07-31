from django.contrib import admin

# Register your models here.
from .models import Product,Available,Order

admin.site.register(Product)
admin.site.register(Available)
admin.site.register(Order)
