# Generated by Django 5.1.5 on 2025-01-27 15:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_api', '0007_rename_enrollment_id_attendance_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, unique=True),
        ),
    ]
