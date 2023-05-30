from django.urls import path

from . import views

app_name = 'garden'#todo what is this
urlpatterns = [
    path('<int:id>', views.GardenAPI.as_view(), name='get_garden_api'),
    path('<int:id>/update', views.GardenUpdateAPI.as_view(), name='update_garden_api'),
    path('create/', views.GardenCreateAPI.as_view(), name='create_garden'),
    path('<int:id>/delete', views.GardenDeleteAPI.as_view(), name='delete_garden'),
]