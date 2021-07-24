from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from accounts.models import User

class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "role", "name", "phone_number", "address", "salary", "created_at")

class AccountRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
    role = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    salary = serializers.IntegerField()

    class Meta:
        model = User
        fields = ("username", "password", "name", "role", "phone_number", "address", "salary")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AccountLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        print(user)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            validation = {
                "access": access_token,
                "refresh": refresh_token,
                "username": user.username,
                "role": user.role
            }

            return validation

        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

