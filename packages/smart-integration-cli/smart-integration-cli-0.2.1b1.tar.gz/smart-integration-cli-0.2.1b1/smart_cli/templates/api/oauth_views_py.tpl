
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from integration_utils.views import BaseCredentialModelViewSet, BaseGetCredentialAPIView

from .models import Credential
from .serializers import CredentialSerializer


class CredentialModelViewSet(BaseCredentialModelViewSet):
    check_credential = False
    with_smart_auth = False
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer

    def create(self, request, format=None):
        """must be implemented"""
        return Response({"status": "error", 'message': "IMPLEMENTED ME"}, status=403)


class GetCredentialAPIView(BaseGetCredentialAPIView):
    check_credential = False
    with_smart_auth = True

    def get_state(self):
        """
        ---
        parameters:
            - Authorization token in headers
            - 'callback_url' in GET params
        """
        user_info = self.get_user_info(self.request)
        user_id = user_info["id"]
        main_user = user_info["username"]

        state = {
            "callback_url": request.GET['callback_url'],
            "user_id": user_id,
            "main_user": main_user,
            "platform_id": request.GET['platform_id']
        }
        return state

    def get_redirect_uri(self):
        return f"https://google.com/?state={self.get_state()}"
