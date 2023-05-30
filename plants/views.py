from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from plants.models import Plant
from plants.serializers import PlantSerializer


class PlantFilter(ListAPIView):
    serializer_class = PlantSerializer
    permission_classes = [AllowAny]
    # It can be safely remove if we only use get_queryset function
    queryset = Plant.objects.filter(is_valid=True)
    lookup_url_kwarg = ['type', 'light_intensity', 'temperature', 'location_type', 'water', 'growth',
                        'attention_need', 'season', 'is_seasonal', 'fragrance', 'pet_compatible',
                        'allergy_compatible', 'edible', ]

    def get_queryset(self):
        filter = {}
        filter['is_valid'] = True
        for field in self.lookup_url_kwarg:
            if self.request.query_params.get(field):
                filter[field] = self.request.query_params[field]
        return Plant.objects.filter(**filter)

