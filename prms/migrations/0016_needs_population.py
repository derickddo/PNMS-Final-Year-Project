# Generated by Django 5.0.6 on 2024-07-02 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prms', '0015_needs_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='needs',
            name='population',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
