from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from .models import Garden
from .serializers import GardenSerializer, GardenUpdateSerializer


class GardenAPI(RetrieveAPIView):
    serializer_class = GardenSerializer
    permission_classes = [AllowAny]
    queryset = Garden.objects.filter(is_verified=True)
    lookup_field = 'id'


class GardenUpdateAPI(UpdateAPIView):
    serializer_class = GardenUpdateSerializer
    permission_classes = [AllowAny] #Todo Change it to IsAuthenticated
    queryset = Garden.objects.filter(is_verified=True)
    lookup_field = 'id'
