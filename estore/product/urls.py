from django.urls import path

from product.views import ProductAPIView

from product.views import OrderCreateAPIView

urlpatterns = [
    path('products', ProductAPIView.as_view(), name='products'),
    path('orders', OrderCreateAPIView.as_view(), name='login')
    ]