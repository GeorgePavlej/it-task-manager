# Generated by Django 3.2.16 on 2023-01-06 12:35

import apps.home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_employee_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.home.models.create_upload_path),
        ),
    ]
