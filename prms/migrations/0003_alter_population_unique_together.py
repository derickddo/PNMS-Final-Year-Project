# Generated by Django 5.0.6 on 2024-05-23 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0002_remove_region_population_alter_district_name_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='population',
            unique_together=set(),
        ),
    ]