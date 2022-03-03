from mimetypes import common_types
from django.contrib import admin

from contacts.models import ContactModel

admin.site.register(ContactModel)
