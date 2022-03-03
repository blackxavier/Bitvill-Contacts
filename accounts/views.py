# from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.generics import UpdateAPIView
from rest_framework.authentication import TokenAuthentication
from accounts.serializers import (
    ChangePasswordSerializer,
    WriteUserProfileSerializer,
    ReadUserProfileSerializer,
    RegistrationSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework import permissions


User = get_user_model()

# Registration view
@api_view(
    [
        "POST",
    ]
)
def RegistrationApiView(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            token = Token.objects.get(user=account).key
            data = {
                "user": {
                    "response": "Account has been created successfully",
                    "email": account.email,
                    "Phone number": account.phone_number,
                },
                "token": {"key": token},
                "status": f"{status.HTTP_201_CREATED} CREATED",
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # confirm the new passwords match

            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response(
                    {"new_password": ["New passwords does not match"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"response": "successfully changed password"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH"])
@permission_classes((permissions.IsAuthenticated,))
def UserProfileView(request):

    try:
        account = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ReadUserProfileSerializer(account)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = WriteUserProfileSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["response"] = "Account update success"
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        serializer = WriteUserProfileSerializer(
            account, data=request.data, partial=True
        )
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["response"] = "Account update success"
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "user_id": user.pk, "email": user.email})
