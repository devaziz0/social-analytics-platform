# Generated by Django 3.0.2 on 2020-04-29 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2048)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2048)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='InstagramReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impressions', models.IntegerField()),
                ('engagement', models.IntegerField()),
                ('date', models.DateField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.InstagramPost')),
            ],
        ),
        migrations.CreateModel(
            name='FacebookReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impressions', models.IntegerField()),
                ('engagement', models.IntegerField()),
                ('date', models.DateField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting.FacebookPost')),
            ],
        ),
    ]
