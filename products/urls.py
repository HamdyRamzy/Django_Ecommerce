from django.urls import path, include

from products import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('<slug:product_slug>/', views.ProductDetail.as_view()),
    path('categories/all/', views.Categories.as_view()),
    path('<slug:category_slug>/<slug:section_slug>/', views.SectionProducts.as_view()),
    path('<slug:category_slug>/<slug:section_slug>/<slug:item_slug>/', views.ItemProducts.as_view()),
]