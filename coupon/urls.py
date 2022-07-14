from django.urls import path, include

from coupon import views

urlpatterns = [
    path('can_use/',  views.can_use),
    path('coupon/',  views.CouponView.as_view()),

]






