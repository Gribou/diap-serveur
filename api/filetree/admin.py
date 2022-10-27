from django.contrib import admin, messages
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from .models import Picture, StaticFile, Page, Folder
from .tasks import index_content


def refresh_file_index(modeladmin, request, queryset):
    index_content.delay(list(queryset.values_list('pk', flat=True).all()))
    modeladmin.message_user(
        request=request,
        message=mark_safe("Indexation des fichiers en cours. Vérifiez le résultat <a href='{}'>ici</a>.".format(
            reverse_lazy('admin:django_celery_results_taskresult_changelist'))),
        level=messages.SUCCESS
    )


refresh_file_index.short_description = "Actualiser l'indexation des fichiers PDF"


class PageInline(admin.StackedInline):
    model = Page
    readonly_fields = ('number', 'url', 'content_index')
    #exclude = ('content_index', )
    can_delete = False
    extra = 0
    max_num = 0


class StaticFileAdmin(admin.ModelAdmin):
    model = StaticFile
    list_display = ('label', 'file', 'is_indexed')
    search_fields = ['label', 'pages__content_index']
    actions = [refresh_file_index]
    inlines = [PageInline]

    def is_indexed(self, obj):
        if obj.pages.exists():
            if any([p.content_index for p in obj.pages.all() if p.content_index == "<erreur>"]):
                return "Erreur"
            return "Oui"
        return "Non"


class FolderInline(admin.StackedInline):
    model = Folder
    filter_horizontal = ['files']


class FolderAdmin(TreeNodeModelAdmin):
    model = Folder
    search_fields = ['label', 'children__label', 'files__label']
    list_display = ['file_count']
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS
    form = TreeNodeForm
    filter_horizontal = ['files']
    # inlines = [FolderInline]

    def file_count(self, obj):
        return obj.files.count()
    file_count.short_description = "Nb Fichiers"


class PictureAdmin(admin.ModelAdmin):
    model = Picture
    list_display = ["ip_address", "file", "creation_date"]
    readonly_fields = ['ip_address', 'file', 'creation_date']


admin.site.register(StaticFile, StaticFileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(Picture, PictureAdmin)
