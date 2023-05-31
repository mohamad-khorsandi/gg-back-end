from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Garden
from .serializers import GardenSerializer, GardenUpdateSerializer, GardenCreateSerializer
from accounts.models import GardenOwnerProfile


class GardenAPI(RetrieveAPIView):
    serializer_class = GardenSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user = GardenOwnerProfile.objects.filter(user=self.request.user)[0]
        garden = user.garden
        return garden


class GardenUpdateAPI(UpdateAPIView):
    serializer_class = GardenUpdateSerializer
    permission_classes = [AllowAny]  # Todo: Change it to IsAuthenticated

    def get_object(self):
        user = GardenOwnerProfile.objects.filter(user=self.request.user)[0]
        garden = user.garden
        return garden


class GardenCreateAPI(CreateAPIView):
    serializer_class = GardenCreateSerializer
    permission_classes = [AllowAny]  # Todo: Change it to IsAuthenticated

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user.is_garden_owner:
            user = GardenOwnerProfile.objects.filter(user=user)[0]
            try:
                garden = user.garden_set
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            except:
                data['garden_owner'] = request.user.id
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)


class GardenDeleteAPI(DestroyAPIView):
    serializer_class = GardenSerializer
    permission_classes = [AllowAny]  # Todo: Change it to IsAuthenticated

    def get_object(self):
        user = GardenOwnerProfile.objects.filter(user=self.request.user)[0]
        garden = user.garden
        return garden

    # def delete(self, request, *args, **kwargs):
    #     data = request.data
    #     user = request.user
    #     if user.is_garden_owner:
    #         garden = Garden.objects.filter(id=self.kwargs['id'])[0]
    #         user = GardenOwnerProfile.objects.filter(user=user)[0]
    #         try:
    #             if garden == user.garden:
    #                 self.perform_destroy(garden)
    #                 return Response(data=data, status=status.HTTP_200_OK)
    #             return Response(data=data, status=status.HTTP_403_FORBIDDEN)
    #         except:
    #             return Response(data=data, status=status.HTTP_403_FORBIDDEN)
    #     return Response(data=data, status=status.HTTP_403_FORBIDDEN)
