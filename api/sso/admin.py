from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from .tasks import refresh_keycloak
from .models import SSOConfig, SSOUserProfile


def refresh_realm(modeladmin, request, queryset):
    result = refresh_keycloak.delay()
    modeladmin.message_user(
        request,
        mark_safe("<a href='{}'>Tâche {} ajoutée à la file</a> ({})".format(
            reverse_lazy('admin:django_celery_results_taskresult_changelist'), result.task_id, result.status))
    )


refresh_realm.short_description = "Actualiser la configuration Keycloak"


class SSOConfigAdmin(admin.ModelAdmin):
    model = SSOConfig
    fields = ['well_known_oidc', 'public_key']
    readonly_fields = ['well_known_oidc', 'public_key']
    actions = [refresh_realm]

    def has_add_permission(self, request):
        # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and SSOConfig.objects.exists():
            retVal = False
        return retVal


class SSOProfileInline(admin.StackedInline):
    model = SSOUserProfile
    readonly_fields = ['sub', 'access_token', 'expires_before',
                       'refresh_token', 'refresh_expires_before']


class CustomUserAdmin(UserAdmin):
    inlines = [SSOProfileInline]
    list_display = UserAdmin.list_display + ('is_sso',)

    def is_sso(self, obj):
        try:
            return obj.sso_profile.sub is not None
        except:
            return False
    is_sso.boolean = True
    is_sso.short_description = "SSO"


admin.site.register(SSOConfig, SSOConfigAdmin)
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.login_template = "sso/login.html"
