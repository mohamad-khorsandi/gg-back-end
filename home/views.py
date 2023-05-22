from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status
from ..plants.models import Plants
from ..plants.serializers import PlantsSerializer


class ExploreAPI(APIView):

    def get(self, request):
        query = Plants.objects.all()
        serializers = PlantsSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

