# Generated by Django 3.0.2 on 2020-04-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0003_auto_20200430_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookpost',
            name='post_id',
            field=models.CharField(max_length=2048, unique=True),
        ),
    ]
