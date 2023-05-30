from django.urls import path

from . import views

app_name = 'plants'#todo what is this
urlpatterns = [
    path('filter/', views.PlantFilter.as_view(), name='explore_api'),
]