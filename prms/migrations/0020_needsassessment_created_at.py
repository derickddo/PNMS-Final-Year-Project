# Generated by Django 5.0.6 on 2024-07-23 19:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0019_populationprojection_is_education_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='needsassessment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]