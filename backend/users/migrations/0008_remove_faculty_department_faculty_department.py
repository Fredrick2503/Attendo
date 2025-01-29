# Generated by Django 5.1.5 on 2025-01-29 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0004_alter_class_room_id'),
        ('users', '0007_remove_student_department_student_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='department',
        ),
        migrations.AddField(
            model_name='faculty',
            name='department',
            field=models.ManyToManyField(to='auth_api.department'),
        ),
    ]
