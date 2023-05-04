from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('verify/', views.UserVerifyCodeView.as_view(), name='verify_code'),
]