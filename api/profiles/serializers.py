from rest_framework import serializers

from api.utils import flatten
from filetree.serializers import FolderSerializer
from search.serializers import SearchApiEndpointSerializer
from . import models


class LayoutElementSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    icon = serializers.FileField()
    folder_pk = serializers.SerializerMethodField()

    class Meta:
        model = models.LayoutElement
        fields = ['title', 'info', 'color',
                  'textColor', 'icon', 'url', 'is_file', 'is_folder', 'folder_pk']

    def get_url(self, obj):
        return obj.url(self.context)

    def get_folder_pk(self, obj):
        return obj.folder.pk if obj.is_folder else None


class FullFolderSerializer(FolderSerializer):
    children = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    class Meta(FolderSerializer.Meta):
        fields = FolderSerializer.Meta.fields + ['children', 'parent']

    def get_children(self, obj):
        elements = [c.element for c in obj.get_children()] + \
            [f.element for f in obj.files.all()]
        return LayoutElementSerializer(elements, many=True, context=self.context).data

    def get_parent(self, obj):
        return obj.parent.pk if obj.parent is not None else None


class LayoutCellSerializer(serializers.ModelSerializer):
    element = LayoutElementSerializer()

    class Meta:
        model = models.LayoutCell
        fields = ['row', 'col', 'element']


class ToolbarCellSerializer(serializers.ModelSerializer):
    element = LayoutElementSerializer()

    class Meta:
        model = models.ToolbarCell
        fields = ['rank', 'element']


class ProfileSerializer(serializers.ModelSerializer):
    folders = serializers.SerializerMethodField()
    toolbar = ToolbarCellSerializer(many=True)
    search_api_endpoints = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = ['url', 'title', 'dark_theme', 'toolbar', 'admin_message',
                  'show_photo_button', 'show_search_field', 'show_profile_switch', 'show_external_indicators', 'folders', 'search_api_endpoints']

    def get_folders(self, obj):
        # layout show only root folders in profile
        # this item shows all folders in tree. it provides additional attr on folders compared to LayoutElementSerializer
        all_root_folders_in_profile = list(obj.layout.filter(
            element__folder__isnull=False)) + list(obj.toolbar.filter(element__folder__isnull=False))
        descendants = flatten([
            [f.element.folder] + f.element.folder.get_descendants()
            for f in all_root_folders_in_profile])
        return {d.pk: FullFolderSerializer(d, context=self.context).data for d in descendants}

    def get_search_api_endpoints(self, obj):
        endpoints = [endpoint for eng in obj.search_engines.all()
                     for endpoint in eng.api_endpoints.all()]
        return SearchApiEndpointSerializer(endpoints, many=True, context=self.context).data


def serialize_profile(profile, cells, context):
    # organize cells as a list of list of cells (rows, cols)
    serialized_cells = LayoutCellSerializer(
        cells.filter(profile=profile).order_by('col'),
        many=True, context=context).data
    rows = sorted(list(dict.fromkeys(
        [c['row'] for c in serialized_cells])))
    layout = []
    for row in rows:
        # serialized_cells is already sorted by col
        layout.append(
            [c['element']
                for c in serialized_cells if c['row'] == row])
    return {
        **ProfileSerializer(profile, context=context).data,
        'layout': layout
    }
