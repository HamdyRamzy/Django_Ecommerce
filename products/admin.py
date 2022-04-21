from django.contrib import admin

from .models import Category, Section, Item, Product

admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Item)
admin.site.register(Product)
