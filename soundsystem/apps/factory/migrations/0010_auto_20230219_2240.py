# Generated by Django 3.2.18 on 2023-02-19 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0009_auto_20230219_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='max_intensity',
            field=models.FloatField(default=10, verbose_name='максимальная допустимая интенсивность'),
        ),
        migrations.AddField(
            model_name='project',
            name='min_intensity',
            field=models.FloatField(default=0, verbose_name='минимальная допустимая интенсивность'),
        ),
    ]