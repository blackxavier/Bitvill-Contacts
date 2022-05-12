from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

User = get_user_model()


class MyAuthTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


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

    def validate_phone_number(self, value):
        qs = User.objects.filter(phone_number=value)
        if qs:
            raise serializers.ValidationError(
                {"error": "Phone number has already been used"}
            )
        else:
            return value

    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if qs:
            raise serializers.ValidationError({"error": "Email has already been used"})
        else:
            return value


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

    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if qs:
            raise serializers.ValidationError({"error": "Email has already been used"})
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
