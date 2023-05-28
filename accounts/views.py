import random

from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from utils import send_otp_code
from . import serializers
from .models import TemporaryUser, NormalUser


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request):
        #todo check that phone number is not repeated
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

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

        return Response(status=status.HTTP_200_OK)


class UserVerifyCodeView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserVerifyCodeSerializer

    def post(self, request):
        serializer = serializers.UserVerifyCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        code = serializer.data['code']

        temp_user = TemporaryUser.objects.filter(code=code)

        if not len(temp_user) == 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        main_user = temp_user[0].to_user()
        main_user.save()
        temp_user.delete()

        token, created = Token.objects.get_or_create(user=main_user)
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        data = request.data
        serializer = serializers.UserLoginSerializer(data=data)

        if serializer.is_valid():
            user = NormalUser.objects.filter(email=data['email'], password=data['password'])

            if user:
                token, created = Token.objects.get_or_create(user=user[0])
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return NormalUser.objects.all()


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(status=status.HTTP_200_OK)
