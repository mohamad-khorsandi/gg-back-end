from rest_framework import serializers
from .models import Plant, PlantImage


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

    def get_image_list(self, obj: Plant):
        return PlantImage.objects.filter(plant=obj)