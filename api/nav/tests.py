from django.test import TestCase, override_settings
import shutil
import os

from api.tests.base import generate_uploaded_file
from .models import TabletAppConfig, AppItem

MEDIA_ROOT_TEST = "media_test"


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class NavSignalsTest(TestCase):

    def setUp(self):
        app = AppItem.objects.create(title="App")
        self.conf = TabletAppConfig.objects.create(
            parent_app=app, icon=generate_uploaded_file("test.png"))
        self.file_path = self.conf.icon.path

    def tearDown(self):
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def test_files_are_deleted_on_model_update(self):
        self.assertTrue(os.path.exists(self.file_path))
        self.conf.icon = generate_uploaded_file("test2.png")
        self.conf.save()
        self.assertFalse(os.path.exists(self.file_path))
        self.assertTrue(os.path.exists(self.conf.icon.path))

    def test_files_are_deleted_on_model_delete(self):
        self.assertTrue(os.path.exists(self.file_path))
        self.conf.delete()
        self.assertFalse(os.path.exists(self.file_path))
