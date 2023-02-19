# Generated by Django 3.2.18 on 2023-02-19 18:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('factory', '0008_auto_20230218_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='measure',
            name='author_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='measure',
            name='data',
            field=models.FileField(upload_to='documents/', verbose_name='данные'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='direct_start',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(0)], verbose_name='минимальный угол обзора'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='direct_stop',
            field=models.IntegerField(default=180, validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(0)], verbose_name='максимальный угол обзора'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='mean_intensity',
            field=models.FloatField(default=0, verbose_name='интенсивность'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='processed_data',
            field=models.FileField(upload_to='documents/', verbose_name='обработанные данные'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_monitored',
            field=models.BooleanField(default=False, verbose_name='мониторинг'),
        ),
    ]
