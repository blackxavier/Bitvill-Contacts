from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegistrationApiView, name="register"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("me/", views.UserProfileView, name="user-profile"),
    path("login/", views.ObtainAuthTokenView.as_view(), name="login"),
]
