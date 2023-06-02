from django.urls import path

from . import views

app_name = 'plants'
urlpatterns = [
    path('filter/', views.PlantFilter.as_view(), name='explore_api'),
    path('<int:id>', views.PlantDetails.as_view(), name='plant_details'),
    path('list/', views.PlantList.as_view(), name='plant_list'),
]
