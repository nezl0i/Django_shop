# Generated by Django 3.2.9 on 2021-12-22 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key_expired',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
