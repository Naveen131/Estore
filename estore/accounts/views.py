from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from accounts.serializer import UserSignUpSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from utils.common import APIResponse

from accounts.serializer import UserLoginSerializer

from accounts.models import User


# Create your views here.

class UserSignUpAPIView(CreateAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
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
            return APIResponse(data=data, status_code=200, message="success")
        except Exception as e:
            return APIResponse(data=None, status_code=400, message=str(e))


class UserLoginAPIView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
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

            user = data.get('user')
            refresh = RefreshToken.for_user(user)

            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),

            }


            return APIResponse(data=token, status_code=200, message="success")
        except Exception as e:
            return APIResponse(data=None, status_code=400, message=str(e))




