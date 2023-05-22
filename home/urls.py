from django.urls import path, include
from . import views

app_name = 'home' # what is this?
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), # what is this again?
    path('home_plants_api', views.ExploreAPI.as_view(), name='explore_api'),
]