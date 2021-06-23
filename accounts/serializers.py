from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import UserProfile

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        profile = UserProfile.objects.get(user=self.user)
        data['role'] = profile.role

        # data['groups'] = self.user.groups.values_list('name', flat=True)
        return data