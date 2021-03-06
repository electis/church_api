# Generated by Django 2.2.17 on 2020-12-26 01:30

from django.db import migrations, models

def site_init(apps, schema_editor):
    Site = apps.get_model('api', 'Site')
    Main = apps.get_model('api', 'Main')
    Profile = apps.get_model('api', 'Profile')
    Form = apps.get_model('api', 'Form')
    NewsSection = apps.get_model('api', 'NewsSection')

    site, create = Site.objects.get_or_create()
    if create:
        Main.objects.update(site=site)
        Profile.objects.update(site=site)
        Form.objects.update(site=site)
        NewsSection.objects.update(site=site)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20201226_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='domain',
            field=models.CharField(default='church22.ru', max_length=64, unique=True),
        ),
        migrations.RunPython(site_init, migrations.RunPython.noop),
    ]
