from rest_framework import serializers

from accounts.models import NormalUser


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = ['email', 'name', 'phone_number', 'password']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserVerifyCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = ['id', 'email', 'name', 'phone_number', 'is_garden_owner', 'image']
