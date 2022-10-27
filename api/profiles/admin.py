from django.contrib import admin

from .models import LayoutCell, Profile, ProfileMapping, ToolbarCell


class TabletLayoutAdmin(admin.TabularInline):
    model = LayoutCell


class ToolbarAdmin(admin.TabularInline):
    model = ToolbarCell
    max_num = 4


@admin.register(Profile)
class TabletProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['title', 'url', 'app_count',
                    'show_photo_button', 'show_search_field', 'show_profile_switch']
    inlines = [TabletLayoutAdmin, ToolbarAdmin]
    filter_horizontal = ('search_engines', 'additional_apps',)

    def app_count(self, obj):
        return obj.layout.count()
    app_count.short_description = "Eléments"

    def get_queryset(self, request):
        if request.resolver_match.func.__name__ == 'change_view':
            return super().get_queryset(request).prefetch_related('layout__element__app__parent_app', 'layout__element__file', 'layout__element__folder', 'search_engines', 'toolbar', 'additional_apps')
        else:
            return super().get_queryset(request)


@admin.register(ProfileMapping)
class TabletMappingAdmin(admin.ModelAdmin):
    model = ProfileMapping
    list_display = ['ip_address', 'profile']
