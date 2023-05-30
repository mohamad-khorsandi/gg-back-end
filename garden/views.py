from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from .models import Garden
from .serializers import GardenSerializer, GardenUpdateSerializer, GardenCreateSerializer


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


class GardenCreateAPI(CreateAPIView):
    serializer_class = GardenCreateSerializer
    permission_classes = [AllowAny]  # Todo Change it to IsAuthenticated

    def create(self, request, *args, **kwargs):
        data = request.data
        data['garden_owner'] = request.user.email
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)


class GardenDeleteAPI(DestroyAPIView):
    serializer_class = GardenSerializer
    permission_classes = [AllowAny]
    queryset = Garden.objects.all()
    lookup_field = 'id'
