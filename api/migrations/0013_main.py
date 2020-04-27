# Generated by Django 2.2.11 on 2020-04-27 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200427_0706'),
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('welcome', models.TextField(blank=True, default='')),
                ('youtube', models.CharField(blank=True, default='', max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
