from rest_framework import serializers
from .models import Garden


class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = '__all__'


class GardenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        exclude = ['garden_owner', 'is_verified', 'business_code',]