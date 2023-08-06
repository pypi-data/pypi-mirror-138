from django.urls import path, re_path
from integration_utils.views import HomeAPIView

from .views import CredentialModelViewSet

urlpatterns = [
    # auth methods
    path(
        'get_credentials/',
        CredentialModelViewSet.as_view({"post": "create"}),
        name='get-credentials',
    ),
    # cred info
    re_path(
        r'^credential/(?P<pk>\d+)/$',
        CredentialModelViewSet.as_view({"get": "retrieve"}),
        name="credential-detail",
    ),
    path(
        'credential-list/',
        CredentialModelViewSet.as_view({"get": "list"}),
        name='credential-list',
    ),
    path('', HomeAPIView.as_view(), name='api'),
]