# Generated by Django 4.1.6 on 2023-02-11 17:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("factory", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="measure",
            name="measure_name",
            field=models.CharField(
                default="дефектовка", max_length=150, verbose_name="название измерения"
            ),
        ),
        migrations.AlterField(
            model_name="measure",
            name="author_name",
            field=models.CharField(max_length=50, verbose_name="автор измерения"),
        ),
    ]
