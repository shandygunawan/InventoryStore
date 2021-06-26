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
from rest_framework.permissions import AllowAny

from accounts.serializers import AccountLoginSerializer


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

