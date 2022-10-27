from django.test import TestCase, override_settings
import shutil
import os

from api.tests.base import *
from filetree.models import StaticFile


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class FiletreeSignalsTest(TestCase):

    def setUp(self):
        self.file = StaticFile.objects.create(file=generate_uploaded_file())
        self.file_path = self.file.file.path

    def tearDown(self):
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def test_files_are_deleted_on_model_update(self):
        self.assertTrue(os.path.exists(self.file_path))
        self.file.file = generate_uploaded_file("test2.txt")
        self.file.save()
        self.assertFalse(os.path.exists(self.file_path))
        self.assertTrue(os.path.exists(self.file.file.path))

    def test_files_are_deleted_on_model_delete(self):
        self.assertTrue(os.path.exists(self.file_path))
        self.file.delete()
        self.assertFalse(os.path.exists(self.file_path))
