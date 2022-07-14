from importlib.resources import path
from django.forms import ValidationError
from .models import Coupon
from .serializers import CouponSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class CouponView(APIView):
    def post(self, request, format=None):
        query = request.GET.get('coupon_code', '')
        try:
            coupon = Coupon.objects.get(code=query)
            if coupon.can_use():
                serializer = CouponSerializer(coupon)
                return Response(serializer.data)
            else:
                return Response("Is not availble")

        except Exception:
            return Response("Is not founded")     

def can_use(request):
    path
