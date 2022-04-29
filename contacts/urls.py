from django.urls import path

from contacts.views import ListCreateApiView, RetrieveUpdateDeleteAPIView

app_name = "contactsapi"

urlpatterns = [
    path("contacts/", ListCreateApiView.as_view(), name="list-create-contact"),
    path(
        "contacts/<int:pk>/",
        RetrieveUpdateDeleteAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
]
