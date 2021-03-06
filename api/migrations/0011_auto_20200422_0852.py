# Generated by Django 2.2.11 on 2020-04-22 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200420_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='html',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='newssection',
            name='icon',
            field=models.CharField(default='mbri-info', max_length=32),
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]
