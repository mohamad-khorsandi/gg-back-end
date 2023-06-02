from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('signup/', views.UserRegistrationView.as_view(), name='user_register'),
    path('verify/', views.UserVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('get-user/', views.GetUser.as_view(), name='get_user'),
    path('update-user/', views.UpdateUser.as_view(), name='update_user'),
    path('update-GardenOwner/', views.UpdateGardenOwner.as_view(), name='update_FardenOwner'),

    path('bookmark-plant/<int:id_plant>', views.SavedPlantList.as_view(), name='saved_plant_list'),
    path('bookmark-list/', views.GetBookmarkList.as_view(), name='bookmark_plant_list'),
    path('remove-saved-plant/<int:id_plant>', views.RemoveSavedPlantView.as_view(), name='remove_saved_plant'),

    path('set-default-condition/', views.UserSetDefaultConditionView.as_view(), name='set_default_condition'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
