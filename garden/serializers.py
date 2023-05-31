from rest_framework import serializers
from .models import Garden
from accounts.serializers import GardenOwnerSerializer
from plants.serializers import PlantSerializer


class GardenSerializer(serializers.ModelSerializer):
    plants = PlantSerializer(many=True)

    class Meta:
        model = Garden
        fields = '__all__'


class GardenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        exclude = ['garden_owner', 'is_verified', 'business_code',]


class GardenCreateSerializer(serializers.ModelSerializer):
   # garden_owner = GardenOwnerSerializer()

    class Meta:
        model = Garden
        exclude = ['is_verified', 'business_code',]
