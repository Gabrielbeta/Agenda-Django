# Generated by Django 3.2.6 on 2021-10-08 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_evento_usuarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='local',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
