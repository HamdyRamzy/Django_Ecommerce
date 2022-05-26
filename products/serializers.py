from rest_framework import serializers

from .models import Category, Section, Item, Product, ProductImage


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
