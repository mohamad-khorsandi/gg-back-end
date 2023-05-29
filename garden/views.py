from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from .models import Garden
from .serializers import GardenSerializer


class GardenAPI(RetrieveAPIView):
    serializer_class = GardenSerializer
    permission_classes = [AllowAny]
    queryset = Garden.objects.filter(is_verified=True)
    lookup_field = 'id'


