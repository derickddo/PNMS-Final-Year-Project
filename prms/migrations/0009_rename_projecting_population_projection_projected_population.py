# Generated by Django 5.0.6 on 2024-05-27 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0008_alter_populationprojection_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projection',
            old_name='projecting_population',
            new_name='projected_population',
        ),
    ]