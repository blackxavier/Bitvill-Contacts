# django imports

from django.db import models

from django.dispatch import receiver

from django.conf import settings
from django.db.models.signals import post_save


# rest_framework imports
from rest_framework.authtoken.models import Token


# imports from app

from accounts.manager import UserManager

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("Phone number"), max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
