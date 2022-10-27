from django.db.models import signals
from django.dispatch import receiver

from filetree.models import StaticFile, Folder
from nav.models import TabletAppConfig
from .models import LayoutElement


@receiver(signals.post_save, sender=TabletAppConfig, dispatch_uid="create_element_for_app")
def create_element_for_app(sender, instance, **kwargs):
    LayoutElement.objects.get_or_create(app=instance)


@receiver(signals.post_save, sender=StaticFile, dispatch_uid="create_element_for_file")
def create_element_for_file(sender, instance, **kwargs):
    LayoutElement.objects.get_or_create(file=instance)


@receiver(signals.post_save, sender=Folder, dispatch_uid="create_element_for_folder")
def create_element_for_folder(sender, instance, **kwargs):
    LayoutElement.objects.get_or_create(folder=instance)

# deletion of LayoutElement is handled by cascade, unique=True
