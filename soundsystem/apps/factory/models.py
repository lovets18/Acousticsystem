import datetime
from django.contrib.auth.models import User, UserManager, Group
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.validators import MaxValueValidator, MinValueValidator
import numpy as np
import pandas as pd

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Project(models.Model):
    project_owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    project_name = models.CharField("название проекта", max_length=150)
    project_description = models.TextField("описание проекта")
    create_date = models.DateTimeField("дата начала проекта")
    update_date = models.DateTimeField("дата изменений проекта")
    is_monitored = models.BooleanField("мониторинг", default=False)
    min_intensity = models.FloatField("минимальная допустимая интенсивность", default=0)
    max_intensity = models.FloatField(
        "максимальная допустимая интенсивность", default=10
    )

    def __str__(self):
        return self.project_name

    def track_intensity(self):
        date_intensity = {
            measure.date: measure.mean_intensity for measure in self.measure_set.all()
        }
        return pd.DataFrame(
            {"date": date_intensity.keys(), "intensity": date_intensity.values()}
        )

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "проекты"


class Measure(models.Model):
    author_name = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    measure_name = models.CharField(
        "название измерения", max_length=150, default="дефектовка"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateTimeField("дата измерения", auto_now_add=True)
    data = models.FileField("данные", upload_to="documents/")
    processed_data = models.FileField("обработанные данные", upload_to="documents/")
    mean_intensity = models.FloatField("интенсивность", default=0)
    direct_start = models.IntegerField(
        "минимальный угол обзора",
        default=0,
        validators=[MaxValueValidator(180), MinValueValidator(0)],
    )
    direct_stop = models.IntegerField(
        "максимальный угол обзора",
        default=180,
        validators=[MaxValueValidator(180), MinValueValidator(0)],
    )

    def __str__(self):
        return self.measure_name

    def was_measured_recently(self, days: int = 1) -> bool:
        return self.date >= (timezone.now() - datetime.timedelta(days=days))

    class Meta:
        verbose_name = "измерение"
        verbose_name_plural = "измерения"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
