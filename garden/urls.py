from django.urls import path

from . import views

app_name = 'garden'
urlpatterns = [
    path('get_garden/', views.GardenAPI.as_view(), name='get_garden_api'),
    path('<int:id>/', views.GardenGetIDAPI.as_view(), name='get_garden_by_id_api'),
    path('update/', views.GardenUpdateAPI.as_view(), name='update_garden_api'),
    path('create/', views.GardenCreateAPI.as_view(), name='create_garden'),
    path('delete/', views.GardenDeleteAPI.as_view(), name='delete_garden'),
    path('<int:id>/add_score/', views.GardenAddScoreAPI.as_view(), name='add_score'),
    path('<int:id>/update_score/', views.GardenScoreUpdateAPI.as_view(), name='update_score'),
    path('<int:id>/delete_score/', views.GardenScoreDeleteAPI.as_view(), name='delete_score'),
]
