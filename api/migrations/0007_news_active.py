# Generated by Django 2.2.11 on 2020-04-14 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200414_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]