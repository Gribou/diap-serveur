from django.db import models
from django.db.models import Q
from api.utils import is_internal
from nav.models import TabletAppConfig
from filetree.models import StaticFile, Folder
from search.models import SearchEngine


class LayoutElementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .select_related('app__parent_app', 'file', 'folder')\
            .prefetch_related('folder__files', 'folder__tn_children')

    def get_by_natural_key(self, app, file, folder):
        return self.get(app=app, file=file, folder=folder)

    def create(self, app, file, folder, **data):
        '''
        LayoutElements are created on post_save signal from App,File and Folder

        But when restoring from a database dump, we create an App/File/Folder, it triggers a LayoutElement creation and then the restoration tries to create a new element with the dump data triggering an IntegrityError
        To solve this, we destroy any existing LayoutElement when create is called
    '''
        if any([app, file, folder]):  # if any of them is not None
            existing_elements = self.get_queryset().filter(
                Q(app=app) | Q(file=file) | Q(folder=folder))
            if existing_elements.exists():
                existing_elements.all().delete()
        return super().create(app=app, file=file, folder=folder, **data)


class LayoutElement(models.Model):
    objects = LayoutElementManager()
    # wrapper element to use StaticFile or TabletAppConfig indifferently
    app = models.OneToOneField(TabletAppConfig,
                               related_name="element",
                               on_delete=models.CASCADE, null=True, blank=True)
    file = models.OneToOneField(StaticFile, related_name="element",
                                on_delete=models.CASCADE, null=True, blank=True)
    folder = models.OneToOneField(Folder, related_name="element",
                                  on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def is_file(self):
        return self.file is not None and self.app is None

    @property
    def is_folder(self):
        return self.folder is not None and not self.is_file

    @property
    def title(self):
        try:
            if self.is_folder:
                return self.folder.label
            if self.is_file:
                return self.file.label
            return self.app.title
        except:
            return "Vide"

    @property
    def color(self):
        try:
            if self.is_folder:
                return self.folder.color
            if self.is_file:
                return self.file.color
            return self.app.color
        except:
            pass

    @property
    def textColor(self):
        try:
            if self.is_folder:
                return self.folder.textColor
            if self.is_file:
                return self.file.textColor
            return self.app.textColor
        except:
            pass

    @property
    def icon(self):
        try:
            if self.is_folder:
                return self.folder.icon
            if self.is_file:
                return self.file.icon
            return self.app.icon
        except:
            pass

    @property
    def info(self):
        try:
            return self.app.info
        except:
            pass

    def url(self, context):
        try:
            if self.is_folder:
                return None
            if self.is_file:
                return context['request'].build_absolute_uri(self.file.file.url)
            if is_internal(context) and self.app.parent_app.internal_url:
                return self.app.parent_app.internal_url
            return self.app.parent_app.external_url
        except:
            pass


class Profile(models.Model):

    url = models.CharField(
        "URL", max_length=20, blank=True, null=True, unique=True, help_text="Lien à utiliser pour accéder à ce profil (ex : mon-profil)")
    title = models.CharField("Titre", max_length=50)
    admin_message = models.CharField(
        "Message de l'administrateur", max_length=100, help_text="Message d'information affiché sur le profil", null=True, blank=True)
    dark_theme = models.BooleanField("Thème sombre", default=True)
    show_photo_button = models.BooleanField(
        "Bouton Appareil Photo", default=False)
    show_search_field = models.BooleanField(
        "Champ de recherche", default=False)
    show_profile_switch = models.BooleanField(
        "Sélecteur de profil", default=True)
    show_external_indicators = models.BooleanField(
        "Indicateurs de liens externes", default=False)
    search_engines = models.ManyToManyField(
        SearchEngine, blank=True, related_name="profiles", verbose_name="Moteurs de recherche")
    additional_apps = models.ManyToManyField(
        TabletAppConfig, blank=True, related_name="profiles_additional",
        help_text="Application non affichées sur la page d'accueil mais utilisables par le moteur de recherche", verbose_name="Applications supplémentaires")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self):
        return self.title


class ToolbarCell(models.Model):
    rank = models.PositiveIntegerField("Ordre", default=0)
    element = models.ForeignKey(
        LayoutElement, related_name="toolbar_cell", null=False, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, related_name="toolbar", null=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ["rank"]
        verbose_name = "Barre d'outils"
        verbose_name_plural = "Barre d'outils"


class LayoutCell(models.Model):
    row = models.PositiveIntegerField("Rangée", default=0)
    col = models.PositiveIntegerField("Colonne", default=0)
    element = models.ForeignKey(
        LayoutElement, related_name="cell", null=False, on_delete=models.CASCADE, limit_choices_to=Q(folder__isnull=True) | Q(folder__tn_parent__isnull=True))
    # do not allow non root folders
    profile = models.ForeignKey(
        Profile, related_name="layout", null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            'row',
            'col',
            'profile'
        )
        ordering = ['row', 'col']
        verbose_name = "Case"
        verbose_name_plural = "Disposition"

    def __str__(self):
        return "{} ({}:{})".format(self.element, self.row, self.col)


class ProfileMapping(models.Model):
    profile = models.ForeignKey(
        Profile, related_name="mappings", null=True, on_delete=models.SET_NULL, verbose_name="Profil")
    ip_address = models.CharField(
        "Adresse IP", max_length=20, null=True, blank=True, help_text="'*' pour indiquer un profil par défaut globalement.")

    class Meta:
        verbose_name = "Mapping Profil-IP"


import profiles.signals  # noqa
