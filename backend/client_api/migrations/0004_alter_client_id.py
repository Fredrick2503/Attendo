# Generated by Django 5.1.5 on 2025-01-30 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_api', '0003_alter_client_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.CharField(default='0b79ec0d15c445978c082bd884b5ef35', max_length=36, primary_key=True, serialize=False, unique=True),
        ),
    ]
