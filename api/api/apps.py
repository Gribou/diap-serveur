from django.apps import AppConfig
from constance.apps import ConstanceConfig
from django_celery_results.apps import CeleryResultConfig
from django_celery_beat.apps import BeatConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


ConstanceConfig.verbose_name = "Paramètres"
# prevent unecessary migration :
ConstanceConfig.default_auto_field = 'django.db.models.AutoField'
CeleryResultConfig.verbose_name = "Tâches - Résultats"
BeatConfig.verbose_name = "Tâches - Planification"
