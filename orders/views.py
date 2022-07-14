from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from coupon.models import Coupon

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        coupon = serializer.validated_data['coupon']
        if coupon != '':
            coupon = Coupon.objects.get(code=coupon)
            if coupon.can_use():
                coupon_value = coupon.value
                coupon.use()
                price = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
                if coupon_value > 0:
                    paid_amount = price - (price * coupon_value / 100)
                else:
                    paid_amount = price
                try:
                    serializer.save(user=request.user, paid_amount=paid_amount, coupon=coupon)

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
                paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
                try:
                    serializer.save(user=request.user, paid_amount=paid_amount)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)