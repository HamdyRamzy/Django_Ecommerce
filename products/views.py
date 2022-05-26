from unicodedata import category
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product, Category, Section, Item
from .serializers import CategorySerializer, ProductSerializer, SectionSerializer
from rest_framework.pagination import PageNumberPagination


class LatestProductsList(APIView):
    def get(self, request, format=None):

        products = Product.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 6
        results = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(results, many=True)

        return paginator.get_paginated_response(serializer.data)


class ProductDetail(APIView):
    def get(self, request, product_slug, format=None):
        product = get_object_or_404(Product, slug=product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class Categories(APIView):
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class SectionProducts(APIView):
    def get(self, request, category_slug, section_slug, format=None):
        products = Product.objects.filter(
            category__slug=category_slug, section__slug=section_slug)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        results = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(results, many=True)

        return paginator.get_paginated_response(serializer.data)


class ItemProducts(APIView):
    def get(self, request, category_slug, section_slug, item_slug, format=None):
        products = Product.objects.filter(
            category__slug=category_slug, section__slug=section_slug, item__slug=item_slug)

        paginator = PageNumberPagination()
        paginator.page_size = 6
        results = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(results, many=True)

        return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query) | Q(section__name__icontains=query) | Q(item__name__icontains=query))
        paginator = PageNumberPagination()
        paginator.page_size = 6
        results = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(results, many=True)

        return paginator.get_paginated_response(serializer.data)
    else:
        return Response({"products": []})

