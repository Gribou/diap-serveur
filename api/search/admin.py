from django.contrib import admin

from .models import SearchApiEndpoint, SearchEngine


class SearchApiEndpointInline(admin.StackedInline):
    model = SearchApiEndpoint


@admin.register(SearchEngine)
class SearchEngineAdmin(admin.ModelAdmin):
    model = SearchEngine
    list_display = ['name', 'template_url', 'api']
    inlines = [SearchApiEndpointInline]

    def api(self, obj):
        return obj.api_endpoints.count()
