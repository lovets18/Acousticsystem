# Generated by Django 3.2.18 on 2023-02-18 14:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("factory", "0007_project_is_monitored"),
    ]

    operations = [
        migrations.AddField(
            model_name="measure",
            name="direct_start",
            field=models.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MaxValueValidator(180),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
        migrations.AddField(
            model_name="measure",
            name="direct_stop",
            field=models.IntegerField(
                default=180,
                validators=[
                    django.core.validators.MaxValueValidator(180),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
        migrations.AddField(
            model_name="measure",
            name="mean_intensity",
            field=models.FloatField(default=0),
        ),
    ]
