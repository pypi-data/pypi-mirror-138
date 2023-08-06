from rest_framework.response import Response
from integration_utils.views import BaseCredentialModelViewSet

from .models import Credential
from .serializers import CredentialSerializer


class CredentialModelViewSet(BaseCredentialModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer

    def create(self, request, format=None):
        """must be implemented"""
        return Response({"status": "error", 'message': "IMPLEMENT ME"}, status=422)
