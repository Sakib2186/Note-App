# Generated by Django 4.2.2 on 2023-12-01 17:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('UserData', '0005_alter_usernotes_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotes',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
