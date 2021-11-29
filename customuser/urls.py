"""Customuser urls."""
app_name = "customuser"
from django.urls import include, path
from rest_framework import routers

from .views import (
    ActivateAccount,
    CustomObtainJSONWebToken,
    PasswordResetConfirmView,
    PasswordResetView,
    UserViewSet,
)

router = routers.DefaultRouter()

from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

urlpatterns = [
    path("", include(router.urls)),
    path("accounts/login/", CustomObtainJSONWebToken.as_view(), name="auth-login"),
    path("accounts/api-token-refresh/", refresh_jwt_token),
    path("api-token-verify/", verify_jwt_token),
    path(
        "accounts/password/reset/",
        PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "accounts/password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path(
        "accounts/activate",
        ActivateAccount.as_view({"get": "activate_account"}),
        name="activate-account",
    ),
]
router.register("accounts/users", UserViewSet, basename="users")
urlpatterns += router.urls
