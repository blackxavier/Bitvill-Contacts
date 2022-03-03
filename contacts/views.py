from rest_framework import generics, status
from contacts.serializers import (
    ReadIndividualContactSerializer,
    ReadContactsSerializer,
    WriteContactSerializer,
)
from contacts.models import ContactModel
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import UpdateAPIView


class ListCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContactModel.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        contacts = self.get_queryset()
        serializer = ReadContactsSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = WriteContactSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            print(serializer.validated_data)
            print(serializer.errors)
            serializer.save(user=request.user)
            return Response(
                {
                    "data": serializer.data,
                    "message": "Contact was created successfuly",
                    "status": f"{status.HTTP_201_CREATED} CREATED",
                }
            )
        else:
            return Response((serializer.errors, status.HTTP_400_BAD_REQUEST))


class RetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ContactModel.objects.all()
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadIndividualContactSerializer
        elif self.requeest.method in ["PUT", "PATCH"]:
            return WriteContactSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return ContactModel.objects.filter(user=self.request.user)
