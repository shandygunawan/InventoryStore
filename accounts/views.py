from django.shortcuts import render

# from rest_framework_simplejwt.views import TokenObtainPairView

# from accounts.serializers import CustomTokenObtainPairSerializer
#
#
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.models import User
from accounts.serializers import (
    AccountListSerializer,
    AccountRegistrationSerializer,
    AccountLoginSerializer
)

class AccountList(APIView):
    serializer_class = AccountListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 'admin':
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)


class AccountRegistration(APIView):
    serializer_class = AccountRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'status_code': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }
            return Response(response, status=status_code)


class AccountLogin(APIView):
    serializer_class = AccountLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'status_code': status_code,
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticated_user': {
                    'username': serializer.data['username'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

