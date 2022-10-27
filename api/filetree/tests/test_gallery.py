from rest_framework import status
import io
from PIL import Image
from django.utils import timezone
from datetime import timedelta

from api.tests.base import *

from filetree.views import PictureViewSet
from filetree.models import Picture
from filetree.tasks import clean_pictures


def generate_photo_file(title="test.png"):
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = title
    file.seek(0)
    return file


class GalleryApiTestCase(ApiTestCase):
    url = "/api/gallery/"

    def setUp(self):
        super().setUp()
        self.mine = Picture.objects.create(
            file=generate_uploaded_file(), ip_address="127.0.0.1")
        self.not_mine = Picture.objects.create(
            file=generate_uploaded_file(), ip_address="192.168.0.1")
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def test_gallery_cleaning(self):
        self.mine.creation_date = timezone.now() - timedelta(hours=3)
        self.mine.save()
        self.not_mine.creation_date = timezone.now()
        self.not_mine.save()
        clean_pictures.delay()
        self.assertFalse(Picture.objects.filter(pk=self.mine.pk).exists())
        self.assertTrue(Picture.objects.filter(pk=self.not_mine.pk).exists())

    def test_create_picture(self):
        '''created object has correct ip address'''
        request = self.factory.post(
            self.url, {'file': generate_photo_file()}, format="multipart")
        response = PictureViewSet.as_view(actions={"post": "create"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Picture.objects.get(
            pk=response.data['pk']).ip_address, "127.0.0.1")

    def test_list_pictures(self):
        '''endpoint provides only picture for the same ip address'''
        request = self.factory.get(self.url)
        response = PictureViewSet.as_view(actions={"get": "list"})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['pk'], self.mine.pk)

    def test_destroy_picture(self):
        '''allowed only if same ip address'''
        request = self.factory.delete(
            "{}{}/".format(self.url, self.not_mine.pk))
        response = PictureViewSet.as_view(
            {"delete": "destroy"})(request, pk=self.not_mine.pk)
        self.assertTrue(status.is_client_error(response.status_code))

        request = self.factory.delete(
            "{}{}/".format(self.url, self.mine.pk))
        response = PictureViewSet.as_view(
            {"delete": "destroy"})(request, pk=self.mine.pk)
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(Picture.objects.filter(pk=self.mine.pk).exists())
