from django.db import models, transaction
from django.shortcuts import render

from product.serializers import ProductViewSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from utils.common import ListAPIViewWithPagination, CustomCreateAPIView

from product.models import Product

from product.serializers import (ProductCreateSerializer, OrderCreateSerializer,
                                 OrderViewSerializer,PizzaViewSerializer)

from utils.common import APIResponse, CustomPagination

from product.models import Pizza

from product.models import PizzaOrder

from product.serializers import PizzaCreateSerializer

from product.serializers import PizzaOrderViewSerializer


# Create your views here.
class ProductAPIView(generics.ListCreateAPIView):
    serializer_class = ProductCreateSerializer
    pagination_class = CustomPagination
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        queryset = self.get_queryset()

        # Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProductViewSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If not paginated, serialize the entire queryset
        serializer = ProductViewSerializer(queryset, many=True)
        return APIResponse(data=serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            errors = []
            for field, messages in serializer.errors.items():
                errors.append(messages[0] if type(messages) == list else messages)

            return APIResponse(data=None, status_code=400,
                               message=errors[0].__str__() if type(
                                   errors[0]) == 'rest_framework.exceptions.ErrorDetail'
                               else errors[0])

        data = serializer.validated_data
        try:
            instance = serializer.create(data)

            data = self.get_serializer(instance).data
            return APIResponse(data=data, status_code=200, message="success")
        except Exception as e:
            return APIResponse(data=None, status_code=400, message=str(e))


# class ProductCreateAPIView(CustomCreateAPIView):
#     serializer_class = ProductCreateSerializer
#
#     def get_view_serializer(self, instance):
#         return ProductViewSerializer(instance)


class OrderCreateAPIView(CustomCreateAPIView):
    serializer_class = OrderCreateSerializer

    def get_view_serializer(self, instance):
        return OrderViewSerializer(instance)


class PizzaAPIListView(generics.RetrieveAPIView):
    serializer_class = PizzaViewSerializer
    queryset = Pizza.objects.all()

    def get(self, request, *args, **kwargs):
        data = request.data
        query_params = self.request.query_params
        try:
            if query_params:
                queryset = Pizza.objects.filter(name__icontains=query_params['name'])
            else:
                queryset = Pizza.objects.all()

            serializer = self.serializer_class()

            data = PizzaViewSerializer(queryset,many=True).data

            return APIResponse(data=data, message='Success',status_code=200)
        except Exception as e:
            return APIResponse(data=None, message=str(e), status_code=500)


class CreateOrderAPIView(CustomCreateAPIView):
    serializer_class = PizzaCreateSerializer
    queryset = PizzaOrder.objects.all()


    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                instance = serializer.create(serializer.validated_data)
                data = PizzaOrderViewSerializer(instance).data
                return APIResponse(data=data, message="Success", status_code=201)
            else:
                return APIResponse(data=None, message=serializer.errors, status_code=400)
        except Exception as e:
            return APIResponse(data=None, message=str(e), status_code=500)