import random

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import plants.serializers
from plants.models import Plant
from utils import send_otp_code
from . import serializers
from .models import TemporaryUser, NormalUser, GardenOwnerProfile


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data
        random_code = random.randint(1000, 9999)  # todo change this to str
        print(random_code)
        #send_otp_code(data['name'], data['email'], random_code)

        last_code = TemporaryUser.objects.filter(email=data['email'])
        if last_code:
            last_code = last_code[0]
            last_code.code = random_code
            last_code.save()
        else:
            TemporaryUser.from_clean_data(data, random_code).save()

        return Response(status=status.HTTP_200_OK)


class UserVerifyCodeView(APIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
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


class GetUser(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer
    queryset = NormalUser.objects.filter(is_active=True)

    def get_object(self):
        return self.request.user


class UpdateUser(UpdateAPIView):
    queryset = NormalUser.objects.filter(is_active=True)
    serializer_class = serializers.UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserSetDefaultConditionView(UpdateAPIView):
    queryset = NormalUser.objects.filter(is_active=True)
    serializer_class = serializers.UserDefaultConditionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer
    queryset = NormalUser.objects.all()


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth
        token.delete()
        return Response(status=status.HTTP_200_OK)


class SavedPlantList(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id_plant):
        user = request.user
        plant = Plant.objects.get(id=id_plant)
        if plant in user.saved_plants.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.saved_plants.add(plant)
        return Response(status=status.HTTP_200_OK)


class GetGardenOwner(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GardenOwnerSerializer
    queryset = NormalUser.objects.filter(is_active=True)

    def get_object(self):
        return self.request.user


class UpdateGardenOwner(UpdateAPIView):
    queryset = GardenOwnerProfile.objects.all()
    serializer_class = serializers.GardenOwnerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.password == old_password:
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            user.password = new_password
            user.save()
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveSavedPlantView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id_plant):
        try:
            plant = request.user.saved_plants.get(id=id_plant)
        except Plant.DoesNotExist:
            return Response('The plant is not in your saved plant list.', status=400)
        request.user.saved_plants.remove(plant)
        return Response('The plant has been removed from your saved plant list.', status=204)


class GetBookmarkList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = plants.serializers.PlantSerializer
    queryset = NormalUser.objects.all()

    def get_queryset(self):
        return self.request.user.saved_plants