# Generated by Django 3.1 on 2023-01-15 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscriptionReference',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
