from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token
from solo.models import SingletonModel
from sorl.thumbnail import ImageField


class Site(models.Model):
    name = models.CharField(max_length=64, default='Барнаул')
    domain = models.CharField(max_length=64, default='church22.ru', unique=True)

    def __str__(self):
        return f'{self.name} - {self.domain}'


class Main(models.Model):
    site = models.OneToOneField(Site, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, default='')
    welcome = models.TextField(default='', blank=True)
    youtube = models.CharField(max_length=16, default='', blank=True)

    def __str__(self):
        return str(self.site)


class Config(SingletonModel):
    tgram = JSONField(default=dict)


class Profile(models.Model):
    class Meta:
        ordering = ('position', 'name',)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, default='')
    birthday = models.DateField(null=True, blank=True)
    function = models.CharField(max_length=255, blank=True, default='')
    image = ImageField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg'))])
    about = models.TextField(blank=True, default='')
    active = models.BooleanField(default=True)
    city = models.CharField(max_length=64, blank=True, default='')
    phone = models.CharField(max_length=32, blank=True, default='')
    phone_visible = models.BooleanField(default=False, blank=True)
    social_email = models.CharField(max_length=64, blank=True, default='')
    social_page = models.CharField(max_length=64, blank=True, default='')
    social_vk = models.CharField(max_length=64, blank=True, default='')
    social_fb = models.CharField(max_length=64, blank=True, default='')
    social_ok = models.CharField(max_length=64, blank=True, default='')
    social_insta = models.CharField(max_length=64, blank=True, default='')
    social_youtube = models.CharField(max_length=64, blank=True, default='')
    telegram = models.CharField(max_length=64, blank=True, default='')
    position = models.SmallIntegerField(default=100)

    def __str__(self):
        return f'{self.position} - {self.name}'


class Form(models.Model):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=32, default='')
    text = models.TextField(default='')
    sended = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class NewsSection(models.Model):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, default='')
    icon = models.CharField(max_length=32, default='mbri-info')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class News(models.Model):
    class Meta:
        ordering = ('-date',)
    section = models.ForeignKey(NewsSection, on_delete=models.SET_NULL, null=True, blank=True)
    author_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now, blank=True)
    title = models.CharField(max_length=255, default='')
    cover = ImageField(null=True, validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg'))])
    image = ImageField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=('jpg', 'jpeg'))])
    text = models.TextField(default='', blank=True)
    html = models.TextField(default='', blank=True)
    youtube = models.CharField(max_length=16, default='', blank=True)
    author = models.TextField(default='', blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
