from django.urls import path

from . import views

app_name = 'garden'#todo what is this
urlpatterns = [
    path('<int:pk>', views.GardenAPI.as_view(), name='explore_api'),
]