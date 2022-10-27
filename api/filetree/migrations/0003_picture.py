# Generated by Django 3.2.10 on 2021-12-07 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filetree', '0002_folder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=250, upload_to='camera', verbose_name='Fichier')),
                ('ip_address', models.CharField(blank=True, help_text="Permet d'identifier le client ayant envoyé l'image", max_length=20, null=True, verbose_name='Adresse IP')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photothèque',
            },
        ),
    ]
