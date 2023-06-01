from rest_framework import serializers
from .models import GardenScore
from accounts.serilaizers import UserScoreSerializer


class ScoreSerializer(serializers.Serializer):
    user = UserScoreSerializer()

    class Meta:
        model = GardenScore
        fields = '__all__'
