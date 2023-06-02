from rest_framework import serializers
from .models import Plant, PlantImage
from garden.models import Garden


class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = '__all__'


class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ['img']


class PlantDetailSerializer(serializers.ModelSerializer):
    images = PlantImageSerializer(many=True)
    gardens = serializers.SerializerMethodField('get_gardens')

    class Meta:
        model = Plant
        fields = '__all__'

    def get_gardens(self, obj):
        gardens = obj.garden_set.filter(is_verified=True)
        return PlantDetailGardenSerializer(gardens, many=True).data


class PlantDetailGardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ['id', 'name', 'avg_score', 'profile_photo']
