from django.test import TestCase, override_settings
import shutil
import os

from api.tests.base import *
from filetree.models import StaticFile


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class FiletreeIndexTest(TestCase):

    def setUp(self):
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def test_pdf_file_content_is_indexed(self):
        f = StaticFile.objects.create(file=generate_dummy_pdf_file())
        f.refresh_from_db()
        self.assertEqual(f.pages.count(), 2)
        self.assertIn("A Simple PDF File", f.pages.first().content_index)
        self.assertIn("The end, and just as well.",
                      f.pages.last().content_index)

    def test_other_file_content_is_not_indexed(self):
        # and does not trigger a crash...
        f = StaticFile.objects.create(file=generate_uploaded_file())
        f.refresh_from_db()
        self.assertEqual(f.pages.count(), 0)

    def test_bad_pdf_file_content_is_not_indexed(self):
        f = StaticFile.objects.create(file=generate_bad_pdf_file())
        f.refresh_from_db()
        self.assertEqual(f.pages.count(), 1)
        self.assertEqual(f.pages.first().content_index, "<erreur>")
