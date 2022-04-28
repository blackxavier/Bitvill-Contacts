from rest_framework import serializers
from rest_framework import status

from django.contrib.auth import get_user_model


from rest_framework.authtoken.models import Token


User = get_user_model()


class ReadUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "email",
            "phone_number",
            "date_joined",
        ]


class WriteUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
        ]


class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        style={"input-type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "phone_number", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_phone_number(self, value):
        qs = User.objects.filter(phone_number=value)
        if qs:
            raise serializers.ValidationError(
                {"error": "Phone number has already been used"}
            )
        else:
            return value

    def save(self):
        account = User(
            email=self.validated_data["email"],
            phone_number=self.validated_data["phone_number"],
        )
        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]

        if password != confirm_password:
            raise serializers.ValidationError({"error": "Passwords don't match"})
        else:
            account.set_password(password)
            account.save()
            return account


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
