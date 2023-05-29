from django.urls import path

from . import views

app_name = 'garden'#todo what is this
urlpatterns = [
    path('<int:id>', views.GardenAPI.as_view(), name='explore_api'),
]