from django.db import models
from django.core.validators import FileExtensionValidator
from treenode.models import TreeNodeModel


class StaticFile(models.Model):
    label = models.CharField(
        'Intitulé', max_length=100, null=False, blank=False)
    file = models.FileField('Fichier PDF', blank=False,
                            null=False, max_length=251, upload_to='files',
                            validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    color = models.CharField("Couleur de fond",
                             null=True,
                             blank=True,
                             max_length=10)
    textColor = models.CharField("Couleur du texte",
                                 null=True,
                                 blank=True,
                                 max_length=10)
    icon = models.FileField("Icône",
                            upload_to='icons',
                            max_length=250,
                            blank=True,
                            help_text="Fichier SVG de préférence")
    # colors and icons are used for Profile layout

    class Meta:
        verbose_name = 'Fichier'
        verbose_name_plural = 'Fichiers'

    def __str__(self):
        return self.label

    # to be used by generic media cleaning signal
    def get_file(self):
        return self.file


class Page(models.Model):
    file = models.ForeignKey(
        StaticFile, related_name='pages', on_delete=models.CASCADE)
    number = models.IntegerField('Numéro de page')
    content_index = models.TextField(blank=True, null=True)

    @property
    def url(self):
        return '{}#page={}'.format(self.file.file.url, self.number)


class Folder(TreeNodeModel):
    treenode_display_field = 'label'
    label = models.CharField(
        "Intitulé", max_length=100, null=False, blank=False)
    color = models.CharField("Couleur de fond",
                             null=True,
                             blank=True,
                             max_length=10)
    textColor = models.CharField("Couleur du texte",
                                 null=True,
                                 blank=True,
                                 max_length=10)
    icon = models.FileField("Icône",
                            upload_to='icons',
                            max_length=250,
                            blank=True,
                            help_text="Fichier SVG de préférence")
    files = models.ManyToManyField(
        StaticFile, related_name='folders', blank=True)

    class Meta (TreeNodeModel.Meta):
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"


class Picture(models.Model):
    file = models.FileField("Fichier", upload_to="camera", max_length=250)
    ip_address = models.CharField(
        "Adresse IP", max_length=20, null=True, blank=True, help_text="Permet d'identifier le client ayant envoyé l'image")
    creation_date = models.DateTimeField("Date de création", auto_now_add=True)

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photothèque"


import filetree.signals  # noqa
