# Generated by Django 5.0.6 on 2024-07-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0014_needsassessment_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='needs',
            name='available',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
