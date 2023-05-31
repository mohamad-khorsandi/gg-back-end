from rest_framework import serializers
from .models import Garden
from accounts.serializers import GardenOwnerSerializer
from plants.serializers import PlantSerializer


class GardenSerializer(serializers.ModelSerializer):
    plants = PlantSerializer(many=True)
    garden_owner = GardenOwnerSerializer()

    class Meta:
        model = Garden
        fields = '__all__'


class GardenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        exclude = ['id', 'garden_owner', 'business_code', 'address', 'avg_score', 'location', 'phone_number']


class GardenCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Garden
        exclude = ['is_verified',]
