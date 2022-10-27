# Generated by Django 3.2.13 on 2022-06-01 10:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filetree', '0003_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='tn_ancestors_count',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Ancestors count'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='tn_children_count',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Children count'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='tn_depth',
            field=models.PositiveIntegerField(default=0, editable=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Depth'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='tn_descendants_count',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Descendants count'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='tn_index',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Index'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='tn_level',
            field=models.PositiveIntegerField(default=1, editable=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='tn_order',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='tn_priority',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)], verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='tn_siblings_count',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Siblings count'),
        ),
    ]