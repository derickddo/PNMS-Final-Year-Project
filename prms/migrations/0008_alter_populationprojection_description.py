# Generated by Django 5.0.6 on 2024-05-27 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0007_rename_baseandprojecting_projection_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='populationprojection',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]