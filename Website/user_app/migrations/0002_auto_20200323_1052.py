# Generated by Django 3.0.4 on 2020-03-23 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
