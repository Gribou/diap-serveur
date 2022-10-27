from rest_framework import parsers
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.parsers import MultiPartParser

from api.utils import get_client_ip
from .serializers import PictureSerializer
from .models import Picture


class PictureViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = PictureSerializer
    model = Picture
    parsers = [MultiPartParser]

    def get_queryset(self, *args, **kwargs):
        # return only the pictures sent by the same device
        ip_address = get_client_ip(self.request)
        return Picture.objects.filter(ip_address=ip_address)
