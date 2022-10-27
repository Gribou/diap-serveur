
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from constance import config

from api.utils import get_client_ip
from .serializers import serialize_profile
from .models import LayoutCell, Profile, ProfileMapping


def get_default_profile(client_address):
    root_query = ProfileMapping.objects.select_related('profile')
    available_profiles = root_query.filter(
        ip_address=client_address)
    if not available_profiles.exists():
        available_profiles = root_query.filter(ip_address="*")
    default_profile = available_profiles.first(
    ).profile if available_profiles.exists() else None
    return default_profile if default_profile is not None else Profile.objects.first()


class ProfileViewSet(ViewSet):

    def list(self, request):
        context = self.make_serializer_context(request)
        client_address = get_client_ip(request)
        default_profile = get_default_profile(client_address)
        cells = LayoutCell.objects.select_related(
            'element__app__parent_app', 'element__file', 'profile').prefetch_related('profile__search_engines__api_endpoints')
        return Response({
            "client_ip": client_address,
            "default_profile": serialize_profile(default_profile, cells, context),
            "profiles": [serialize_profile(p, cells, context) for p in Profile.objects.all()]
        })

    def make_serializer_context(self, request):
        return {
            "request": request, 'internal_hostname': config.INTERNAL_HOSTNAME
        }
