from django.dispatch.dispatcher import receiver
from django.db.models import signals

from api.utils import delete_file_on_instance_delete, delete_old_file_on_instance_update
from .models import StaticFile
from .tasks import index_content, is_pdf_file

signals.post_delete.connect(delete_file_on_instance_delete,
                            sender=StaticFile,
                            dispatch_uid="delete_file_on_file_delete")
signals.pre_save.connect(delete_old_file_on_instance_update,
                         sender=StaticFile,
                         dispatch_uid="delete_old_file_on_file_update")


@receiver(signals.pre_save, sender=StaticFile, dispatch_uid="reset_index_on_file_update")
def reset_search_index_on_file_update(sender, instance, **kwargs):
    '''delete previous file if it is being updated'''
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False
    if instance.file != old_file:
        # clear page index if file changes
        instance.pages.all().delete()


@receiver(signals.post_save, sender=StaticFile, dispatch_uid="update_page_index")
def update_doc_search_index(sender, instance, **kwargs):
    if is_pdf_file(instance.file) and not instance.pages.exists():
        index_content.delay([instance.pk])
