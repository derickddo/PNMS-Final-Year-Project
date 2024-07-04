# Generated by Django 5.0.6 on 2024-07-03 20:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('prms', '0016_needs_population'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('standard', models.IntegerField()),
                ('required', models.IntegerField()),
                ('new_need', models.IntegerField(blank=True, null=True)),
                ('suplus', models.IntegerField(blank=True, null=True)),
                ('available', models.PositiveBigIntegerField(blank=True, null=True)),
                ('population', models.PositiveBigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'equipment_type',
            },
        ),
        migrations.CreateModel(
            name='FacilityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('standard', models.IntegerField()),
                ('required', models.IntegerField()),
                ('new_need', models.IntegerField(blank=True, null=True)),
                ('suplus', models.IntegerField(blank=True, null=True)),
                ('available', models.PositiveBigIntegerField(blank=True, null=True)),
                ('population', models.PositiveBigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'facility_type',
            },
        ),
        migrations.CreateModel(
            name='FurnitureType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('standard', models.IntegerField()),
                ('required', models.IntegerField()),
                ('new_need', models.IntegerField(blank=True, null=True)),
                ('suplus', models.IntegerField(blank=True, null=True)),
                ('available', models.PositiveBigIntegerField(blank=True, null=True)),
                ('population', models.PositiveBigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OtherType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PersonnelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('standard', models.IntegerField()),
                ('required', models.IntegerField()),
                ('new_need', models.IntegerField(blank=True, null=True)),
                ('suplus', models.IntegerField(blank=True, null=True)),
                ('available', models.PositiveBigIntegerField(blank=True, null=True)),
                ('population', models.PositiveBigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'personnel_type',
            },
        ),
        migrations.RenameField(
            model_name='needs',
            old_name='required',
            new_name='object_id',
        ),
        migrations.RemoveField(
            model_name='needs',
            name='available',
        ),
        migrations.RemoveField(
            model_name='needs',
            name='facility_type',
        ),
        migrations.RemoveField(
            model_name='needs',
            name='new_need',
        ),
        migrations.RemoveField(
            model_name='needs',
            name='population',
        ),
        migrations.RemoveField(
            model_name='needs',
            name='standard',
        ),
        migrations.RemoveField(
            model_name='needs',
            name='suplus',
        ),
        migrations.RemoveField(
            model_name='needs',
            name='year',
        ),
        migrations.AddField(
            model_name='needs',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='needs',
            name='needs_type',
            field=models.CharField(choices=[('facility', 'Facility'), ('personnel', 'Personnel'), ('equipment', 'Equipment'), ('furniture', 'Furniture'), ('others', 'Others')], default='facility', max_length=50),
        ),
    ]
