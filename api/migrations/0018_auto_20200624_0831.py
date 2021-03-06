# Generated by Django 2.2.13 on 2020-06-24 01:31

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20200514_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgram', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='news',
            name='author_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Profile'),
        ),
        migrations.AlterField(
            model_name='news',
            name='cover',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'jpeg'))]),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'jpeg'))]),
        ),
        migrations.AlterField(
            model_name='news',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.NewsSection'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'jpeg'))]),
        ),
    ]
