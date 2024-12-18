from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import User


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username',)


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, error_messages={"required": "Username is required"})
    email = serializers.EmailField(required=True, error_messages={"required": "email is required"})
    password = serializers.CharField(required=True, error_messages={"required": " Username is required"})

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False,error_messages={"username": "email is required"})
    password = serializers.CharField(required=True, allow_null=False, error_messages={"username": "Username is required"})

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # user = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("User Does not exist")

        elif not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        attrs['user'] = user

        return attrs


