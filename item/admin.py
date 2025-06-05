from django.contrib import admin

# Register your models here.

from .models import Category, Item, Discount

admin.site.register(Discount)
admin.site.register(Category)
admin.site.register(Item)