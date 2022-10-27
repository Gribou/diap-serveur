from django.db import models


class AppItem(models.Model):
    title = models.CharField("Titre", max_length=100)
    internal_url = models.CharField(
        "URL interne",
        max_length=250,
        blank=True,
        null=True,
        help_text="URL pour l'accès en interne (Laisser vide si c'est la même que celle pour l'accès externe)."
    )
    external_url = models.CharField(
        "URL externe",
        max_length=250,
        null=True,
        blank=True,
        help_text="URL pour l'accès depuis l'extérieur (Laisser vide si pas d'accès possible)"
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Application"
        verbose_name_plural = "Applications"




class TabletAppConfig(models.Model):
    parent_app = models.OneToOneField(AppItem,
                                      related_name="tablet_config",
                                      on_delete=models.CASCADE)
    tablet_title = models.CharField(
        "Titre sur tablette",
        max_length=100,
        null=True,
        blank=True,
        help_text="Si différent du titre de l'application")
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
    info = models.TextField(
        "Informations",
        blank=True,
        null=True,
        help_text="S'afficheront dans un fenêtre de dialogue en touchant une icône ⓘ")

    def __str__(self):
        return self.tablet_title if self.tablet_title else self.parent_app.title

    def get_file(self):
        return self.icon

    @property
    def title(self):
        return self.tablet_title if self.tablet_title else self.parent_app.title


import nav.signals  # noqa
