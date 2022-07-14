from django.contrib import admin

from .models import Category, Section, Item, Product, ProductImage, Review

admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Item)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
