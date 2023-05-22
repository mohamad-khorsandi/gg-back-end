from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions, status
from plants.models import Plants
from plants.serializers import PlantsSerializer


class ExploreAPI(ListAPIView):
    serializer_class = PlantsSerializer
    permission_classes = [AllowAny]
    queryset = Plants.objects.all()

