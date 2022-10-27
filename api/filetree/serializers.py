from rest_framework import serializers
from rest_framework.settings import api_settings

from api.utils import get_client_ip
from .models import Page, Picture, StaticFile, Folder


class StaticFileSerializer(serializers.ModelSerializer):
    url = serializers.FileField(source='file')
    title = serializers.CharField(source='label')

    class Meta:
        model = StaticFile
        fields = ['title', 'url', 'color', 'textColor', 'icon']


class FolderSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="label")

    class Meta:
        model = Folder
        fields = ['title', 'color', 'textColor', 'icon', 'pk']


class PageSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['title', 'url', 'number', 'color']

    def get_title(self, obj):
        return "{} p.{}".format(obj.file.label, obj.number)

    def get_color(self, obj):
        return obj.file.color

    def get_url(self, obj):
        request = self.context['request']
        search_query = request.query_params.get(
            api_settings.SEARCH_PARAM, None)
        page_url = request.build_absolute_uri(obj.url)
        return "{}&search={}".format(page_url, search_query) if search_query is not None else page_url


class PictureSerializer(serializers.ModelSerializer):
    ip_address = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Picture
        fields = ['file', 'ip_address', 'pk']

    def create(self, validated_data):
        validated_data['ip_address'] = get_client_ip(self.context['request'])
        return super().create(validated_data)
