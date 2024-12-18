from django.db import models, transaction
from django.shortcuts import render

from product.serializers import ProductViewSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from utils.common import ListAPIViewWithPagination, CustomCreateAPIView

from product.models import Product

from product.serializers import ProductCreateSerializer, OrderCreateSerializer, OrderViewSerializer

from utils.common import APIResponse, CustomPagination


# Create your views here.
class ProductAPIView(generics.ListCreateAPIView):
    serializer_class = ProductCreateSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
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
