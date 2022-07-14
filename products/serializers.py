from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Section, Item, Product, ProductImage, Review

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "get_image",
        )


class ProductSerializer(serializers.ModelSerializer):
    imageproduct = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "category",
            "section",
            "item",
            "imageproduct",
            "id",
            "code",
            "rating",
            "name",
            "get_absolute_url",
            "description",
            "price_before_discount",
            "price",
            "get_image",
            "get_thumbnail",
            "in_stock"
        )
        depth = 1

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Review
        fields = (
            "user",
            "product",
            "comment",
            "date_added",
            "rating"
        )


class ItemSerializer(serializers.ModelSerializer):
    productitem = ProductSerializer(many=True)

    class Meta:
        model = Item
        fields = (
            "productitem",
            "id",
            "name",
            "get_absolute_url",
        )


class SectionSerializer(serializers.ModelSerializer):
    itemsection = ItemSerializer(many=True)

    class Meta:
        model = Section
        fields = (
            "category",
            "id",
            "name",
            "get_absolute_url",
            "itemsection",
        )


class CategorySerializer(serializers.ModelSerializer):
    sectioncategory = SectionSerializer(many=True)
    itemcategory = ItemSerializer(many=True)
    productcategory = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "sectioncategory",
            "itemcategory",
            "productcategory",
        )
