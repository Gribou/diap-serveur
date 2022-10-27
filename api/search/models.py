from django.db import models

from nav.models import TabletAppConfig

API_TYPES = [
    ('DIAPASON', 'Diapason'),
    ('MEDIAWIKI', 'Mediawiki')
]


class SearchEngine(models.Model):
    template_url = models.CharField(
        "Modèle d'URL", help_text="{root_url} sera remplacé par l'url de l'application. {search_query} sera remplacé par la recherche de l'utilisateur", null=False, max_length=255)
    name = models.CharField("Nom", null=False, max_length=100)
    parent_app = models.ForeignKey(TabletAppConfig, related_name="app",
                                   on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Moteur de recherche"
        verbose_name_plural = "Moteurs de recherche"

    def make_search_url(self, search_query, context):
        try:
            root_url = self.parent_app.element.url(context)
        except:
            pass
        return self.template_url.replace("{search_query}", search_query).replace("{root_url}", root_url or '')

    def __str__(self):
        return self.name

    @property
    def color(self):
        try:
            return self.parent_app.color
        except:
            pass

    @property
    def textColor(self):
        try:
            return self.parent_app.textColor
        except:
            pass

    @property
    def icon(self):
        try:
            return self.parent_app.icon
        except:
            pass


class SearchApiEndpoint(models.Model):
    search_engine = models.ForeignKey(
        SearchEngine, related_name="api_endpoints", on_delete=models.CASCADE, null=True)
    api_type = models.CharField("Type d'API", max_length=25, choices=API_TYPES)
    template_url = models.CharField(
        "Modèle d'URL", help_text="{root_url} sera remplacé par l'url de l'application. Ne pas renseigner la partie après '?' de l'url.", null=False, max_length=255)
    label = models.CharField("Libellé", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Accès par API"
        verbose_name_plural = "Accès par API"

    def make_url(self, context):
        try:
            root_url = self.search_engine.parent_app.element.url(context)
        except:
            pass
        return self.template_url.replace("{root_url}", root_url or '')

    @property
    def color(self):
        try:
            return self.search_engine.color
        except:
            pass

    @property
    def textColor(self):
        try:
            return self.search_engine.textColor
        except:
            pass

    @property
    def icon(self):
        try:
            return self.search_engine.icon
        except:
            pass
