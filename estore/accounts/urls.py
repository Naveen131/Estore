from django.urls import path

from accounts.views import UserSignUpAPIView, UserLoginAPIView

urlpatterns = [
    path('signup', UserSignUpAPIView.as_view(), name='signup'),
    path('login', UserLoginAPIView.as_view(), name='login')
    ]