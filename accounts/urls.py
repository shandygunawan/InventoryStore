from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from accounts.views import (
    AccountLogin,
    AccountRegistration,
    AccountList,
    AccountDetail,
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name="token-create"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token-refresh"),
    path('login/', AccountLogin.as_view(), name="account-login"),
    path('register/', AccountRegistration.as_view(), name="account-registration"),
    path('accounts/', AccountList.as_view(), name="account-list"),
    path(r'accounts/<int:account_id>/', AccountDetail.as_view(), name='account-update'),
]