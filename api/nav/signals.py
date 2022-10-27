from django.db.models import signals

from api.utils import delete_file_on_instance_delete, delete_old_file_on_instance_update
from .models import TabletAppConfig


signals.post_delete.connect(delete_file_on_instance_delete,
                            sender=TabletAppConfig,
                            dispatch_uid="delete_file_on_profile_delete")
signals.pre_save.connect(delete_old_file_on_instance_update,
                         sender=TabletAppConfig,
                         dispatch_uid="delete_old_file_on_profile_update")
