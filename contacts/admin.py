from mimetypes import common_types

from django.contrib import admin

from contacts.models import ContactModel


class ContactModelAdmin(admin.ModelAdmin):

    list_display = (
        "contact_email",
        "contact_phone_number",
    )
    list_filter = ("contact_email", "date_created")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "contact_email",
                    "contact_phone_number",
                    "contact_first_name",
                    "contact_last_name",
                    "contact_description",
                )
            },
        ),
        # ("Dates", {"fields": ("date_created", "date_modified")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "contact_email",
                    "contact_phone_number",
                    "contact_first_name",
                    "contact_last_name",
                    "contact_description",
                ),
            },
        ),
    )
    search_fields = ("contact_email",)
    ordering = ("contact_email",)


admin.site.register(ContactModel, ContactModelAdmin)
