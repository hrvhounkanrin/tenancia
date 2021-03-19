"""Customuser urls."""
app_name = "customuser"
from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    LogoutView,
    ActivateAccount

)

router = routers.DefaultRouter()
router.register('accounts/users', UserViewSet, basename='users')
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token
)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/login/', obtain_jwt_token, name="auth-login"),
    path('accounts/api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('accounts/password/reset/', PasswordResetView.as_view(),
         name='rest_password_reset'),
    path('accounts/password/reset/confirm/', PasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),
    path('accounts/password/change/', PasswordChangeView.as_view(),
         name='rest_password_change'),
    path('accounts/logout/', LogoutView.as_view(), name='rest_logout'),
    path(
     "accounts/activate",
        ActivateAccount.as_view({"get": "activate_account"}),
        name="activate-account",
    )





]
urlpatterns += router.urls
