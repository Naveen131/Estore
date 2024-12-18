from django.db import transaction, models
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


class APIResponse(JsonResponse):
    def __init__(self, data=None, status_code=200, message="Request succeeded", **kwargs):
        # Check if the status code indicates success or failure
        is_success = 200 <= status_code < 300


        response_data = {
            "status": "success" if is_success else "error",
            "message": message,
            "data": data,
            "status_code":status_code
        }
        if kwargs:
            response_data.update(kwargs)

        super().__init__(data=response_data, status=status_code)


class CustomPagination(PageNumberPagination):
    default_page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # import pdb;pdb.set_trace()
        pagination_data = {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        }

        # Remove keys with None values
        pagination_data = {k: v for k, v in pagination_data.items() if v is not None}

        return APIResponse(data=data, status_code=200, message="Request succeeded", **pagination_data)


class CreateUpdateMixin:
    def create(self, validated_data):
        # import pdb;pdb.set_trace()
        if 'user' in [field.name for field in self.Meta.model._meta.get_fields()]:

            validated_data['user'] = self.context['request'].user

        validated_data['created_by'] = self.context['request'].user

        validated_data['created_at'] = timezone.now()
        # import pdb;pdb.set_trace()

        instance = self.Meta.model.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user

        validated_data['updated_at'] = timezone.now()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class ListAPIViewWithPagination(generics.ListCreateAPIView):
    pagination_class = CustomPagination
    #permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        queryset = self.get_queryset()

        # Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If not paginated, serialize the entire queryset
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(data=serializer.data)


    @transaction.atomic
    def create(self, request, *args, **kwargs):
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
            if isinstance(instance, dict):
                return APIResponse(data=instance, status_code=200, message="success")

            elif isinstance(instance, models.Model):
                data = self.get_serializer(instance).data
                return APIResponse(data=data, status_code=200, message="success")
            return APIResponse(data=data, status_code=200, message="success")
        except Exception as e:
            return APIResponse(data=None, status_code=400, message=str(e))

    def get_serializer(self, instance):
        raise NotImplementedError("Subclasses must implement this method")


class CustomCreateAPIView(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            errors = []
            for field, messages in serializer.errors.items():
                errors.append(messages[0] if type(messages) == list else messages)

            return APIResponse(data=None, status_code=400,
                               message=errors[0].__str__() if type(errors[0])=='rest_framework.exceptions.ErrorDetail'
                               else errors[0])

        data = serializer.validated_data
        try:
            instance = serializer.create(data)
            if isinstance(instance, dict):
                return APIResponse(data=instance, status_code=200, message="success")

            elif isinstance(instance, models.Model):
                data = self.get_view_serializer(instance).data
                return APIResponse(data=data, status_code=200, message="success")
            return APIResponse(data=data, status_code=200, message="success")
        except Exception as e:
            return APIResponse(data=None, status_code=400, message=str(e))

    def get_view_serializer(self, instance):
        raise NotImplementedError("Subclasses must implement this method")


class CustomRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAuthenticated]
    # lookup_field = 'pk'

    def get_view_serializer(self, instance):
        raise NotImplementedError("Subclasses must implement this method")

    def get(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        try:
            instance = self.get_object()
            data = self.get_view_serializer(instance).data
            return APIResponse(data=data, message='success', status_code=200)
        except Exception as e:
            return APIResponse(data=None, message="Object Does not exist", status_code=400)

    @transaction.atomic
    def put(self, request, *args, **kwargs):

        instance = self.get_object()

        if not instance:
            return APIResponse(data=None, message="Object Does not exist", status_code=400)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            errors = []
            for field, messages in serializer.errors.items():
                errors.extend((messages[0] if type(messages) == list else messages))

            return APIResponse(data=None, status_code=400,
                               message=errors[0].__str() if type(errors[0])=='rest_framework.exceptions.ErrorDetail'
                               else errors[0])

        data = serializer.validated_data
        try:
            instance = serializer.update(instance, data)
            data = self.get_view_serializer(instance).data
            return APIResponse(data=data, status_code=200, message="success")
        except Exception as e:
            return APIResponse(data=None, status_code=400, message=str(e))

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return APIResponse(data=None, status_code=200, message="success")
