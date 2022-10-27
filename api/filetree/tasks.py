from celery import shared_task
from celery.exceptions import Ignore
from django.apps import apps
from django.utils import timezone
from django.core.files.storage import default_storage
from datetime import timedelta
import os
import tempfile
import xml.etree.ElementTree as ET


def _get_file_model():
    return apps.get_model(app_label='filetree', model_name='StaticFile')


def _get_page_model():
    return apps.get_model(app_label='filetree', model_name='Page')


def pdftoxml(pdf_file, options=""):
    """converts pdf file to xml file"""
    # NEEDS 'pdftohtml' to be installed on host/container (see Dockerfile)
    xmlin = tempfile.NamedTemporaryFile(
        mode='r', suffix='.xml', encoding="latin-1")
    tmpxml = xmlin.name  # "temph.xml"
    cmd = 'pdftohtml -xml -nodrm -zoom 1.5 -enc Latin1 -noframes %s "%s" "%s"' % (
        options, pdf_file.path, os.path.splitext(tmpxml)[0])
    # can't turn off output, so throw away even stderr yeuch
    cmd = cmd + " >/dev/null 2>&1"
    os.system(cmd)
    # xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata.encode("latin-1")


def parse_xml_to_pages(file_object, xmldata_string):
    Page = _get_page_model()
    try:
        root = ET.fromstring(xmldata_string)
        page_number = 1
        for page in root.iter('page'):
            page_content = ' '.join([s.replace('\n', '')
                                    for s in page.itertext()]).strip()
            # create page even if no content so that an indexed file always as at least one page
            # otherwise, signals keeps triggering index task
            Page.objects.create(
                file=file_object, number=page_number,
                content_index=page_content)
            page_number += 1
    except Exception as e:
        # create at least one page so that signals does not trigger index task again
        if not file_object.pages.exists():
            Page.objects.create(file=file_object, number=1,
                                content_index="<erreur>")
        raise e


def is_pdf_file(pdf_file):
    return pdf_file is not None and os.path.splitext(pdf_file.name)[1][1:].lower() == "pdf"


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 5})
def index_content(self, pk_list):
    File = _get_file_model()
    for file_pk in pk_list:
        file = File.objects.get(pk=file_pk)
        file.pages.all().delete()
        if not default_storage.exists(file.file.path):
            # mark task as failed
            self.update_state(
                state='FAILURE', meta="File {} not present in storage".format(file.label))
            raise Ignore()
        elif not is_pdf_file(file.file):
            # mark stask as failed
            self.update_state(
                state='FAILURE', meta="File {} is not PDF".format(file.label))
            raise Ignore()
        else:
            parse_xml_to_pages(file, pdftoxml(file.file))

    return "OK"


@shared_task
def clean_pictures():
    apps.get_model("filetree", "Picture").objects.filter(
        creation_date__lte=timezone.now() - timedelta(hours=2)).delete()
