# Generated by Django 2.2.11 on 2020-04-27 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20200422_0852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-date',)},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='news',
            name='youtube',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='news',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.NewsSection'),
        ),
    ]
