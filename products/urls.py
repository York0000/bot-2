from django.urls import path

from products.views import CategoryListAPIView, ProductListAPIView, ProductRetrieveAPIView, OrderCreateAPIView

app_name = 'products'

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<int:pk>/', ProductListAPIView.as_view()),
    path('search/', ProductListAPIView.as_view()),
    path('cart-data/', ProductListAPIView.as_view()),
    path('orders/create/', OrderCreateAPIView.as_view()),
    path('products/<int:pk>/', ProductRetrieveAPIView.as_view()),
]
