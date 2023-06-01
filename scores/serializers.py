from rest_framework import serializers
from .models import GardenScore
from accounts.serializers import UserScoreSerializer


class ScoreSerializer(serializers.ModelSerializer):
    user = UserScoreSerializer()

    class Meta:
        model = GardenScore
        fields = '__all__'


class ScoreAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = GardenScore
        fields = '__all__'
