from rest_framework import serializers

from accounts.models import NormalUser, GardenOwnerProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = ['email', 'name', 'phone_number', 'password', 'is_garden_owner']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserVerifyCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = ['id', 'email', 'name', 'phone_number', 'is_garden_owner', 'image']


class GardenOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GardenOwnerProfile
        fields = '__all__'


class UserScoreSerializer(serializers.Serializer):
    class Meta:
        model = NormalUser
        fields = ['name', 'image']
