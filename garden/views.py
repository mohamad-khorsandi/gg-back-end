from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Garden
from .serializers import GardenSerializer, GardenUpdateSerializer, GardenCreateSerializer


class GardenAPI(RetrieveAPIView):
    serializer_class = GardenSerializer
    permission_classes = [AllowAny]
    queryset = Garden.objects.filter(is_verified=True)
    lookup_field = 'id'


class GardenUpdateAPI(UpdateAPIView):
    serializer_class = GardenUpdateSerializer
    permission_classes = [AllowAny]  # Todo: Change it to IsAuthenticated
    queryset = Garden.objects.filter(is_verified=True)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user.is_garden_owner:  # Todo: Chang it if needed
            garden = self.get_object()
            if user.objects.garden == garden:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)  # todo: check if it is correct
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)


class GardenCreateAPI(CreateAPIView):
    serializer_class = GardenCreateSerializer
    permission_classes = [AllowAny]  # Todo: Change it to IsAuthenticated

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user.is_garden_owner:  # Todo: Chang it if needed
            if user.objects.garden is None:
                data['garden_owner'] = request.user
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)  # todo: checl if it is correct
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)


class GardenDeleteAPI(DestroyAPIView):
    serializer_class = GardenSerializer
    permission_classes = [AllowAny]  # Todo: Change it to IsAuthenticated
    queryset = Garden.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user.is_garden_owner:
            garden = self.get_object()
            if garden == user.objects.garden:
                self.perform_destroy(garden)
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)
