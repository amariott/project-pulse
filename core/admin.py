from django.contrib import admin

# Register your models here.

from .models import UserProfile, Order, OrderItem, Review

admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)