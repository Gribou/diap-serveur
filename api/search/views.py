from rest_framework.viewsets import ViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.db.models import Q
from constance import config

from profiles.models import LayoutElement
from profiles.serializers import LayoutElementSerializer
from profiles.views import get_client_ip, get_default_profile
from filetree.models import Page, StaticFile, Folder
from filetree.serializers import PageSerializer, StaticFileSerializer, FolderSerializer
from .models import SearchEngine
from .serializers import SearchEngineSerializer


class SimpleSearchFilter(SearchFilter):
    # utility class to use without a view
    default_search_fields = []

    def __init__(self, search_fields):
        super().__init__()
        self.default_search_fields = search_fields

    def get_search_fields(self, view, request):
        return self.default_search_fields


def search(search_fields, queryset, request):
    return SimpleSearchFilter(search_fields).filter_queryset(request, queryset, None)


APP_SEARCH_FIELDS = ['app__tablet_title', 'app__parent_app__title']
FILE_SEARCH_FIELDS = ['label', 'file']
PAGE_SEARCH_FIELDS = ['content_index']
FOLDER_SEARCH_FIELDS = ['label']


class SearchViewSet(ViewSet):
    PROFILE_KEY = "profile"

    def list(self, request):
        context = {"request": request,
                   'internal_hostname': config.INTERNAL_HOSTNAME}
        profile = self.get_profile_from_request(request)
        profile_folders = self.get_all_profile_folders(profile)
        profile_files = self.get_all_files_of_profile(profile, profile_folders)
        results = {
            "folders": self.get_folder_results(request, context, profile_folders),
            "files": self.get_file_results(request, context, profile_files),
            "pages": self.get_page_results(request, context, profile_files),
            "apps": self.get_app_results(request, context, profile),
            "others": self.get_other_results(context, profile),
        }
        is_empty = results['files']['count'] + len(results['apps']) + len(
            results['folders']) + len(results['others']) == 0
        return Response({'is_empty': is_empty, **results})

    def get_profile_from_request(self, request):
        # profile name from query_params else default profile for this ip
        return request.query_params.get(
            self.PROFILE_KEY,
            get_default_profile(get_client_ip(request)).url)

    def get_app_results(self, request, context, profile):
        # return only apps from the current profile
        queryset = search(APP_SEARCH_FIELDS, LayoutElement.objects.filter(
            Q(app__isnull=False),
            Q(cell__profile__url=profile) | Q(app__profiles_additional__url=profile) | Q(toolbar_cell__profile__url=profile)), request).distinct()
        elements = LayoutElementSerializer(
            queryset, many=True, context=context).data
        # filter elements with empty url
        return [elt for elt in elements if elt['url'] is not None]

    def get_all_profile_folders(self, profile):
        # root folders and all their children
        root_folders = Folder.get_roots_queryset()\
            .filter(Q(element__cell__profile__url=profile) | Q(element__toolbar_cell__profile__url=profile))
        return Folder.objects.filter(pk__in=[c.pk for f in root_folders for c in f.get_descendants()] + [f.pk for f in root_folders])

    def get_all_files_of_profile(self, profile, folders):
        # files in folders and files at root of profile
        return StaticFile.objects.filter(Q(pk__in=[file.pk for folder in folders for file in folder.files.all()]) | Q(element__cell__profile__url=profile) | Q(element__toolbar_cell__profile__url=profile))

    def get_all_pages_of_files(self, files):
        return Page.objects.filter(file__in=files)

    def get_file_results(self, request, context, profile_files):
        MAX_FILE_RESULTS = 10
        result_files = search(FILE_SEARCH_FIELDS, profile_files, request)
        return {
            'count': result_files.count(),
            'results': StaticFileSerializer(result_files.all(), many=True,
                                            context=context).data[:MAX_FILE_RESULTS]
        }

    def get_page_results(self, request, context, profile_files):
        MAX_FILE_RESULTS = 10
        profile_pages = self.get_all_pages_of_files(profile_files)
        result_pages = search(PAGE_SEARCH_FIELDS, profile_pages, request)
        return {
            'count': result_pages.count(),
            'results': PageSerializer(result_pages.all(), many=True,
                                      context=context).data[:MAX_FILE_RESULTS]
        }

    def get_folder_results(self, request, context, folders):
        folders = search(FOLDER_SEARCH_FIELDS, folders, request)
        return FolderSerializer(folders.all(), many=True, context=context).data

    def get_other_results(self, context, profile):
        engines = SearchEngineSerializer(
            SearchEngine.objects.filter(profiles__url__contains=profile, api_endpoints__isnull=True), many=True, context=context).data
        # filter engines with empty urls
        return [eng for eng in engines if eng['url'] is not None]
