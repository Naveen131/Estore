from django.urls import path

from product.views import ProductAPIView

from product.views import OrderCreateAPIView, PizzaAPIListView, CreateOrderAPIView

urlpatterns = [
    path('products', ProductAPIView.as_view(), name='products'),
    # path('orders', OrderCreateAPIView.as_view(), name='login'),
    path('menu', PizzaAPIListView.as_view(), name='menu'),
    path('orders', CreateOrderAPIView.as_view(), name='pizza-order')
    ]