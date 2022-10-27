import os


def is_internal(context):
    internal_hostname = context.get(
        'internal_hostname', None)
    return internal_hostname == "*" or context.get(
        'request').get_host() in internal_hostname


def flatten(t):
    return [item for sublist in t for item in sublist]


def delete_file_on_instance_delete(sender, instance, **kwargs):
    ''' delete media file on doc delete'''
    try:
        if instance.get_file():
            if os.path.isfile(instance.get_file().path):
                os.remove(instance.get_file().path)
    except:
        pass


def delete_old_file_on_instance_update(sender, instance, **kwargs):
    '''delete previous file if it is being updated'''
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).get_file()
    except sender.DoesNotExist:
        return False

    new_file = instance.get_file()
    if old_file and not old_file == new_file and "media/default/" not in old_file.path:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    return x_forwarded_for.split(',')[-1].strip() if x_forwarded_for is not None else request.META.get("REMOTE_ADDR", None)
