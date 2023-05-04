import random

from django.contrib.auth import login, logout
from rest_framework import permissions, authentication, status
from rest_framework import response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils import send_otp_code, Response
from . import serializers
from .models import TemporaryUser, User


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response.bad_request()

        data = serializer.data
        random_code = random.randint(1000, 9999)  # todo change this to str
        print(random_code)
        send_otp_code(data['name'], data['email'], random_code)

        last_code = TemporaryUser.objects.filter(email=data['email'])
        if last_code:
            last_code = last_code[0]
            last_code.code = random_code
            last_code.save()
        else:
            TemporaryUser.from_clean_data(data, random_code).save()

        return Response.ok()


class UserVerifyCodeView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserVerifyCodeSerializer

    def post(self, request):
        serializer = serializers.UserVerifyCodeSerializer(data=request.data)
        if not serializer.is_valid():
            Response.bad_request()
        code = serializer.data['code']

        temp_user = TemporaryUser.objects.filter(code=code)

        if not len(temp_user) == 1:
            return Response.bad_request()

        main_user = temp_user[0].to_user()
        main_user.save()
        temp_user.delete()

        login(request, main_user)
        return Response.ok()


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.SessionAuthentication]
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        data = request.data
        serializer = serializers.UserLoginSerializer(data=data)

        if serializer.is_valid():
            # todo why django.contrib.auth authenticate not working?
            user = User.objects.filter(email=data['email'], password=data['password'])

            if user:
                login(request, user[0])
                return Response.ok()
            else:
                return Response.unauthorized()

        else:
            return Response.ok()


class UserView(ListAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request):
        logout(request)
        return response.Response(status=status.HTTP_200_OK)
