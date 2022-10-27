from django.contrib import admin
from django.forms.models import ModelForm

from .models import AppItem, TabletAppConfig


class MarkNewInstancesAsChangedModelForm(ModelForm):
    def has_changed(self):
        """ Should returns True if data differs from initial. 
        By always returning true even unchanged inlines will get validated and saved."""
        return not self.instance.pk or super().has_changed()


class TabletAppInline(admin.StackedInline):
    model = TabletAppConfig
    verbose_name = "Affichage sur tablette"
    form = MarkNewInstancesAsChangedModelForm


@admin.register(AppItem)
class AppItemAdmin(admin.ModelAdmin):
    model = AppItem
    list_display = [
        "title", "url", "has_internal_access", "has_external_access",
    ]
    inlines = [TabletAppInline]

    def url(self, obj):
        return obj.internal_url or obj.external_url

    def has_internal_access(self, obj):
        return obj.internal_url is not None or obj.external_url is not None

    has_internal_access.boolean = True
    has_internal_access.short_description = "Accès en interne"

    def has_external_access(self, obj):
        return obj.external_url is not None

    has_external_access.boolean = True
    has_external_access.short_description = "Accès en externe"
