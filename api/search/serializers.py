from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import SearchApiEndpoint, SearchEngine


class SearchApiEndpointSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    icon = serializers.FileField()
    app_url = serializers.SerializerMethodField()

    class Meta:
        model = SearchApiEndpoint
        fields = ['api_type', 'url', 'label',
                  'icon', 'color', 'textColor', 'app_url']

    def get_url(self, obj):
        return obj.make_url(self.context)

    def get_app_url(self, obj):
        search_query = self.context.get('request').query_params.get(
            api_settings.SEARCH_PARAM, '')
        return obj.search_engine.make_search_url(search_query or "{search_query}", self.context)


class SearchEngineSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    icon = serializers.FileField()
    # api_endpoints = SearchApiEndpointSerializer(many=True)

    class Meta:
        model = SearchEngine
        fields = ['name', 'color', 'icon', 'textColor', 'url', 'api_endpoints']

    def get_url(self, obj):
        search_query = self.context.get('request').query_params.get(
            api_settings.SEARCH_PARAM, '')
        return obj.make_search_url(search_query or "{search_query}", self.context)
