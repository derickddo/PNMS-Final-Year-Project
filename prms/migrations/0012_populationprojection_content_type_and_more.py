# Generated by Django 5.0.6 on 2024-06-02 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('prms', '0011_populationprojection_user_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='populationprojection',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='populationprojection',
            name='object_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar.png', null=True, upload_to=''),
        ),
    ]
