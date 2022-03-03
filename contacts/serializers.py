from rest_framework import serializers
from contacts.models import ContactModel


class ReadContactsSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContactModel
        fields = [
            "url",
            "contact_email",
            "fullname",
            "contact_phone_number",
            "date_created",
            "date_modified",
        ]

        read_only_fields = fields

    def get_url(self, obj):
        # retrieve request params and pass it to the get_api_url method
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def get_fullname(self, obj):
        # concatenate the 'contact_first_name' and 'contact_last_name'
        return f"{obj.contact_first_name} {obj.contact_last_name}"


class ReadIndividualContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        fields = [
            "contact_email",
            "contact_first_name",
            "contact_last_name",
            "contact_phone_number",
            "contact_description",
        ]

        read_only_fields = fields


class WriteContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        fields = [
            "contact_email",
            "contact_first_name",
            "contact_last_name",
            "contact_phone_number",
            "contact_description",
        ]

    def validate(self, attrs):
        user = self.context["request"].user
        allcontacts = ContactModel.objects.filter(user=user)
        for contact in allcontacts:
            if contact.contact_email == attrs["contact_email"]:
                raise serializers.ValidationError(
                    {
                        "response": "Contact with this email address  has been saved by you"
                    }
                )
            elif contact.contact_phone_number == attrs["contact_phone_number"]:
                raise serializers.ValidationError(
                    {"response": "Contact with this phone number has been saved by you"}
                )

        return super().validate(attrs)
