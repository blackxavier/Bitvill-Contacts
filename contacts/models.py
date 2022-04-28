from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse


User = get_user_model()


class ContactModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    contact_first_name = models.CharField(max_length=200)
    contact_last_name = models.CharField(max_length=200)
    contact_phone_number = models.CharField(max_length=15)

    contact_description = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_email

    def get_api_url(self, request=None):
        return reverse(
            "contacts:retrieve-update-destroy",
            kwargs={"pk": self.pk},
            request=request,
        )

    class Meta:
        verbose_name_plural = "Contacts"
