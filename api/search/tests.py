from rest_framework import status
from api.tests.base import *
from filetree.models import StaticFile, Page
from search.views import SearchViewSet


class SearchViewTestCase(ApiTestCase):
    url = "/api/search/"

    def _search(self, params={}):
        request = self.factory.get(self.url, params)
        return SearchViewSet.as_view(actions={"get": "list"})(request)

    def test_search_default_profile(self):
        response = self._search({'search': "Tagada"})
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(response.data['is_empty'])
        self.assertEqual(response.data['folders'], [])
        self.assertEqual(response.data['files']['results'], [])
        self.assertEqual(response.data['apps'], [])
        self.assertEqual(response.data['others'], [])

    def test_search_profile_by_name(self):
        response = self._search({'search': "Tagada", 'profile': 'atco'})
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(response.data['is_empty'])
        self.assertEqual(response.data['folders'], [])
        self.assertEqual(response.data['files']['results'], [])
        self.assertEqual(response.data['apps'], [])
        self.assertEqual(response.data['others'][0]["name"], "eNews")
        self.assertTrue(response.data['others'][0]["url"].endswith(
            "/enews/docs?search=Tagada"))

    def test_search_profile_for_folder(self):
        response = self._search({'search': "Dossier", 'profile': 'atco'})
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(response.data['is_empty'])
        self.assertEqual(response.data['folders'][0]['title'], "Dossier")

    def test_search_profile_for_file(self):
        response = self._search({'search': "Fichier", 'profile': 'atco'})
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(response.data['is_empty'])
        self.assertEqual(response.data['files']['count'], 1)
        self.assertEqual(response.data['files']
                         ['results'][0]['title'], "Fichier")

    def test_search_profile_for_file_content(self):
        file = StaticFile.objects.first()
        Page.objects.create(file=file, number=3, content_index=lorem.text())
        response = self._search({'search': "lorem", 'profile': 'atco'})
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(response.data['is_empty'])
        self.assertEqual(response.data['pages']['count'], 1)
        self.assertEqual(response.data['pages']
                         ['results'][0]['title'], "Fichier p.3")
