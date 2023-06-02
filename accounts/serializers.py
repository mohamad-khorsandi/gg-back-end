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


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = ['name', 'phone_number']


class GardenOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GardenOwnerProfile
        fields = '__all__'


class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = ['name', 'image']


class UserDefaultConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalUser
        fields = ['light_condition', 'have_allergy', 'location_type_condition', 'attention_need',
                  'have_pet']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

