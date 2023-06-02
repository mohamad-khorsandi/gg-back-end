from rest_framework import serializers
from .models import Garden
from accounts.serializers import GardenOwnerSerializer
from plants.serializers import PlantSerializer
from scores.serializers import ScoreSerializer
from accounts.serializers import UserSerializer


class GardenByIDSerializer(serializers.ModelSerializer):
    plants = PlantSerializer(many=True)
    user_name = serializers.SerializerMethodField('get_user')
    scores = ScoreSerializer(many=True)
    is_owner = serializers.SerializerMethodField('get_is_owner')

    class Meta:
        model = Garden
        fields = '__all__'

    def get_user(self, obj):
        return UserSerializer(obj.garden_owner.user).data['name']

    def get_is_owner(self, obj):
        req_user = self.context.get('user')
        if req_user == obj.garden_owner.user:
            return True
        else:
            return False


class GardenSerializer(serializers.ModelSerializer):
    plants = PlantSerializer(many=True)
    garden_owner = GardenOwnerSerializer()
    scores = ScoreSerializer(many=True)

    class Meta:
        model = Garden
        fields = '__all__'


class GardenUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Garden
        exclude = ['id', 'garden_owner', 'business_code', 'address', 'avg_score', 'location', 'phone_number',
                   'is_verified', ]


class GardenCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Garden
        exclude = ['is_verified', ]
