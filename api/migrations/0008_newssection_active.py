# Generated by Django 2.2.11 on 2020-04-14 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_news_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='newssection',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
