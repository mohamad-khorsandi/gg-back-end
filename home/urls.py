from django.urls import path, include
from . import views

app_name = 'Home'
urlpatterns = [
    path('home_explore_api/', views.ExploreAPI.as_view(), name='explore_api'),
]