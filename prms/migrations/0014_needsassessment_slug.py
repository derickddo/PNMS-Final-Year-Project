# Generated by Django 5.0.6 on 2024-07-01 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0013_needs_alter_user_options_alter_district_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='needsassessment',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
