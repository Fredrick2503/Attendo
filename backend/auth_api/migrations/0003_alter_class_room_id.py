# Generated by Django 5.1.5 on 2025-01-27 03:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0002_class_room_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class_room',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
