# Generated by Django 5.0.6 on 2024-06-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateField(default='2025-06-11'),
            preserve_default=False,
        ),
    ]