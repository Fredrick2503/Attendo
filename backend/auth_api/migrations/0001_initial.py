# Generated by Django 5.1.5 on 2025-01-26 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('dept_id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=50)),
            ],
        ),
    ]
