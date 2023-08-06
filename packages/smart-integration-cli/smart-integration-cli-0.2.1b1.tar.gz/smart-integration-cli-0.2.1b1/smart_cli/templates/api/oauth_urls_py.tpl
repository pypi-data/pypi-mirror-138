from django.urls import path, re_path
from integration_utils.views import HomeAPIView

from .views import CredentialModelViewSet, GetCredentialAPIView

urlpatterns = [
    # auth methods
    path('get_credentials/', GetCredentialAPIView.as_view(), name='get-credentials'),
    path('token/', CredentialModelViewSet.as_view({"get": "create"}), name='token'),
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
