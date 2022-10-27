from django.test import TestCase, override_settings
from django.core.management import call_command
from rest_framework.test import APIRequestFactory
from contextlib import contextmanager
from django.core.files.uploadedfile import SimpleUploadedFile
import lorem
import shutil

import logging
import sys

from profiles.populate import populate as populate_profiles
from sso.populate import populate as populate_sso
from .data import APPS, DEFAULT_PROFILE, SEARCH_ENGINES, GRID
from nav.models import AppItem, TabletAppConfig
from profiles.models import Profile, LayoutCell, LayoutElement
from search.models import SearchEngine
from filetree.models import StaticFile, Folder


@contextmanager
def streamhandler_to_console(lggr):
    # Use 'up to date' value of sys.stdout for StreamHandler,
    # as set by test runner.
    stream_handler = logging.StreamHandler(sys.stdout)
    lggr.addHandler(stream_handler)
    yield
    lggr.removeHandler(stream_handler)


def testcase_log_console(lggr):
    def testcase_decorator(func):
        def testcase_log_console(*args, **kwargs):
            with streamhandler_to_console(lggr):
                return func(*args, **kwargs)

        return testcase_log_console

    return testcase_decorator


logger = logging.getLogger('django')
# use with @testcase_log_console(logger)

MEDIA_ROOT_TEST = "media_test"


@override_settings(MEDIA_ROOT=(MEDIA_ROOT_TEST + "/media"))
class ApiTestCase(TestCase):

    def tearDown(self):
        logging.disable(logging.NOTSET)
        try:
            shutil.rmtree(MEDIA_ROOT_TEST)
        except OSError:
            pass

    def setUp(self):
        logging.disable(logging.ERROR)
        self.factory = APIRequestFactory()
        populate_profiles()
        populate_sso()

        for app in APPS.values():
            values = app.copy()
            tablet_config = values.pop("tablet", None)
            instance = AppItem.objects.create(**values)
            if tablet_config:
                TabletAppConfig.objects.create(
                    parent_app=instance, **tablet_config)

        self.profile = Profile.objects.create(
            url=DEFAULT_PROFILE, title=DEFAULT_PROFILE.upper(), dark_theme=True)
        app_instances = {
            key:  LayoutElement.objects.filter(
                app__parent_app__title=a['title']).first()
            for key, a in APPS.items()
        }
        for row, apps in enumerate(GRID):
            for col, app_key in enumerate(apps):
                try:
                    LayoutCell.objects.create(
                        element=app_instances[app_key], row=row, col=col, profile=self.profile)
                except:
                    pass

        for engine in SEARCH_ENGINES:
            app = TabletAppConfig.objects.filter(
                parent_app__title=engine['name'])
            if app.exists():
                SearchEngine.objects.create(
                    parent_app=app.first(), **engine)
        self.profile.search_engines.set(SearchEngine.objects.all())

        file = StaticFile.objects.create(
            label="Fichier", file=generate_uploaded_file(),
            icon=generate_uploaded_file(title="icon.svg"), color="#ff0")
        folder = Folder.objects.create(
            label="Dossier", icon=generate_uploaded_file(title="folder_icon.png"))
        folder.files.set([file])
        LayoutCell.objects.create(
            element=LayoutElement.objects.get(file=file), row=3, col=0, profile=self.profile)
        LayoutCell.objects.create(
            element=LayoutElement.objects.get(folder=folder), row=3, col=1, profile=self.profile)
        self.profile.refresh_from_db()


def generate_uploaded_file(title='test.txt', content=lorem.text()):
    return SimpleUploadedFile(
        title, content.encode('utf-8'), content_type="text/plain")


def generate_dummy_pdf_file():
    return SimpleUploadedFile("dummy.pdf", DUMMY_PDF.encode("utf-8"), content_type="application/pdf")


def generate_bad_pdf_file():
    return SimpleUploadedFile("bad.pdf", lorem.text().encode("utf-8"), content_type="application/pdf")


DUMMY_PDF = """%PDF-1.3
%����

1 0 obj
<<
/Type /Catalog
/Outlines 2 0 R
/Pages 3 0 R
>>
endobj

2 0 obj
<<
/Type /Outlines
/Count 0
>>
endobj

3 0 obj
<<
/Type /Pages
/Count 2
/Kids [ 4 0 R 6 0 R ] 
>>
endobj

4 0 obj
<<
/Type /Page
/Parent 3 0 R
/Resources <<
/Font <<
/F1 9 0 R 
>>
/ProcSet 8 0 R
>>
/MediaBox [0 0 612.0000 792.0000]
/Contents 5 0 R
>>
endobj

5 0 obj
<< /Length 1074 >>
stream
2 J
BT
0 0 0 rg
/F1 0027 Tf
57.3750 722.2800 Td
( A Simple PDF File ) Tj
ET
BT
/F1 0010 Tf
69.2500 688.6080 Td
( This is a small demonstration .pdf file - ) Tj
ET
BT
/F1 0010 Tf
69.2500 664.7040 Td
( just for use in the Virtual Mechanics tutorials. More text. And more ) Tj
ET
BT
/F1 0010 Tf
69.2500 652.7520 Td
( text. And more text. And more text. And more text. ) Tj
ET
BT
/F1 0010 Tf
69.2500 628.8480 Td
( And more text. And more text. And more text. And more text. And more ) Tj
ET
BT
/F1 0010 Tf
69.2500 616.8960 Td
( text. And more text. Boring, zzzzz. And more text. And more text. And ) Tj
ET
BT
/F1 0010 Tf
69.2500 604.9440 Td
( more text. And more text. And more text. And more text. And more text. ) Tj
ET
BT
/F1 0010 Tf
69.2500 592.9920 Td
( And more text. And more text. ) Tj
ET
BT
/F1 0010 Tf
69.2500 569.0880 Td
( And more text. And more text. And more text. And more text. And more ) Tj
ET
BT
/F1 0010 Tf
69.2500 557.1360 Td
( text. And more text. And more text. Even more. Continued on page 2 ...) Tj
ET
endstream
endobj

6 0 obj
<<
/Type /Page
/Parent 3 0 R
/Resources <<
/Font <<
/F1 9 0 R 
>>
/ProcSet 8 0 R
>>
/MediaBox [0 0 612.0000 792.0000]
/Contents 7 0 R
>>
endobj

7 0 obj
<< /Length 676 >>
stream
2 J
BT
0 0 0 rg
/F1 0027 Tf
57.3750 722.2800 Td
( Simple PDF File 2 ) Tj
ET
BT
/F1 0010 Tf
69.2500 688.6080 Td
( ...continued from page 1. Yet more text. And more text. And more text. ) Tj
ET
BT
/F1 0010 Tf
69.2500 676.6560 Td
( And more text. And more text. And more text. And more text. And more ) Tj
ET
BT
/F1 0010 Tf
69.2500 664.7040 Td
( text. Oh, how boring typing this stuff. But not as boring as watching ) Tj
ET
BT
/F1 0010 Tf
69.2500 652.7520 Td
( paint dry. And more text. And more text. And more text. And more text. ) Tj
ET
BT
/F1 0010 Tf
69.2500 640.8000 Td
( Boring.  More, a little more text. The end, and just as well. ) Tj
ET
endstream
endobj

8 0 obj
[/PDF /Text]
endobj

9 0 obj
<<
/Type /Font
/Subtype /Type1
/Name /F1
/BaseFont /Helvetica
/Encoding /WinAnsiEncoding
>>
endobj

10 0 obj
<<
/Creator (Rave \(http://www.nevrona.com/rave\))
/Producer (Nevrona Designs)
/CreationDate (D:20060301072826)
>>
endobj

xref
0 11
0000000000 65535 f
0000000019 00000 n
0000000093 00000 n
0000000147 00000 n
0000000222 00000 n
0000000390 00000 n
0000001522 00000 n
0000001690 00000 n
0000002423 00000 n
0000002456 00000 n
0000002574 00000 n

trailer
<<
/Size 11
/Root 1 0 R
/Info 10 0 R
>>

startxref
2714
%%EOF
"""
