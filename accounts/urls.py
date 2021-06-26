from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from accounts.views import (
    AccountLogin
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name="token-create"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token-refresh"),
    path('login/', AccountLogin.as_view(), name="account-login")
]