from django.test import TestCase
from rest_framework import status
from constance.test import override_config

from api.tests.base import *
from filetree.models import Folder
from .models import LayoutElement, LayoutCell, ProfileMapping
from .views import ProfileViewSet


class ProfileModelTestCase(TestCase):

    def test_unique_layout_element(self):
        # test that LayoutElement works properly even if the element already exists
        folder = Folder.objects.create(label="Label")
        self.assertTrue(LayoutElement.objects.filter(folder=folder).exists())
        existing_pk = folder.element.pk
        new_element = LayoutElement.objects.create(
            folder=folder, app=None, file=None, pk=existing_pk+10)
        self.assertTrue(folder.element.pk == new_element.pk)


class ProfileViewTestCase(ApiTestCase):
    url = "/api/profile/"

    def _list_profiles(self):
        request = self.factory.get(self.url)
        return ProfileViewSet.as_view(actions={"get": "list"})(request)

    def test_available_profiles(self):
        response = self._list_profiles()
        self.assertTrue(status.is_success(response.status_code))
        self.assertIn("client_ip", response.data)
        self.assertEqual(response.data['default_profile']['url'], "demo")
        self.assertEqual(['demo', 'atco'], [p['url']
                         for p in response.data['profiles']])
        app_element = response.data['profiles'][1]['layout'][0][1]
        self.assertIsNotNone(app_element['url'])
        self.assertFalse(app_element['is_file'])
        self.assertFalse(app_element['is_folder'])
        file_element = response.data['profiles'][1]['layout'][-1][0]
        self.assertIsNotNone(file_element['url'])
        self.assertTrue(file_element['is_file'])
        self.assertFalse(file_element['is_folder'])
        folder_element = response.data['profiles'][1]['layout'][-1][1]
        self.assertIsNone(folder_element['url'])
        self.assertFalse(folder_element['is_file'])
        self.assertTrue(folder_element['is_folder'])

    def test_empty_layout_element(self):
        '''empty layoutelement is serialized properly'''
        element = LayoutElement.objects.create(
            app=None, file=None, folder=None)
        LayoutCell.objects.create(
            element=element, row=5, col=5, profile=self.profile)
        response = self._list_profiles()
        self.assertTrue(status.is_success(response.status_code))
        empty_element = response.data['profiles'][1]['layout'][-1][0]
        self.assertEqual(empty_element['title'], 'Vide')
        self.assertFalse(empty_element['is_file'])
        self.assertFalse(empty_element['is_folder'])
        self.assertIsNone(empty_element['url'])

    def test_profile_mapping(self):
        '''default profile depends on mapping'''
        ProfileMapping.objects.create(
            profile=self.profile, ip_address="127.0.0.1")
        response = self._list_profiles()
        self.assertEqual(response.data['default_profile']['url'], "atco")

    @override_config(INTERNAL_HOSTNAME="testserver")
    def test_internal_urls(self):
        '''if hostname is internal, show internal urls'''
        response = self._list_profiles()
        app_element = response.data['profiles'][1]['layout'][0][0]
        self.assertIsNotNone(app_element['url'])
