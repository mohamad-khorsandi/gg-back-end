from rest_framework import serializers
from .models import Plant, PlantImage


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

    image_list = serializers.SerializerMethodField()

    def get_image_list(self, obj: Plant):
        return [PlantImageSerializer(image).data for image in PlantImage.objects.filter(plant=obj)]


class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ['img']
