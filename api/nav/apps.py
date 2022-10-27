from django.apps import AppConfig
from constance.apps import ConstanceConfig


class NavConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nav'
    verbose_name = "Applications"


ConstanceConfig.verbose_name = "Paramètres"
ConstanceConfig.default_auto_field = 'django.db.models.AutoField'
