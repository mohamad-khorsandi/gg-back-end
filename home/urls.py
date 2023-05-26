from django.urls import path, include
from . import views

app_name = 'Home'
urlpatterns = [
    path('home_explore_api/', views.PlantFilterAPI.as_view(), name='explore_api'),
]