import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.core.mail.message import EmailMultiAlternatives

from api import models


class TGram:

    @staticmethod
    def get_token(phraze=False):
        if not settings.configured:
            settings.configure()
        if phraze:
            if not settings.TGRAM_PHRAZE:
                raise Exception('Phraze not set')
            return settings.TGRAM_PHRAZE
        if not settings.TGRAM_TOKEN:
            raise Exception('Token not set')
        return settings.TGRAM_TOKEN

    @staticmethod
    def say2boss(text):
        boss_id = models.Config.get_solo().tgram.get('boss_id')
        if not boss_id:
            print('BOSS not found')
            return None
        return TGram.send_message(text, boss_id)

    @staticmethod
    def send_message(text, chat_id, parse_mode='Markdown'):
        try:
            response = requests.get(f'https://api.telegram.org/bot{TGram.get_token()}/sendMessage', params=dict(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode
            ))
        except Exception as Ex:
            print(Ex)
            return False
        else:
            if response.status_code == 200:
                return response.json()
            else:
                print(f'status_code {response.status_code}')
                return False

def get_set(item: str):
    if not settings.configured:
        settings.configure()
    if hasattr(settings, item):
        return getattr(settings, item)


def send_email(title, text, emails: iter = ('andrey@ngbarnaul.ru',), as_html: bool = False):
    mail = EmailMultiAlternatives(title, text, settings.EMAIL_HOST_USER, emails)
    if as_html:
        mail.content_subtype = "html"
    try:
        mail.send(fail_silently=False)
    except Exception as Ex:
        return Ex


def fill_social(profile: models.Profile):
    social_account = SocialAccount.objects.filter(user=profile.user).first()
    if social_account:
        data = social_account.extra_data
        if social_account.provider == 'vk':
            profile.social_vk = f'https://vk.com/id{data["id"]}'
            profile.name = f"{data.get('first_name', '')} {data.get('last_name', '')}"
            profile.city = data['city'].get('title', '') if data.get('city') else ''
            if data.get('bdate'):
                profile.birthday = datetime.strptime(data.get('bdate'), '%d.%m.%Y').date()
            if data.get('email'):
                profile.social_email = data['email']
            if data.get('photo_max_orig'):
                save_image(profile, data['photo_max_orig'], social_account.provider)
        elif social_account.provider == 'odnoklassniki':
            profile.social_ok = f'https://ok.ru/profile/{data["uid"]}'
            profile.name = data.get('name', '')
            profile.city = data['location'].get('city', '') if data.get('location') else ''
            if data.get('birthday'):
                profile.birthday = datetime.strptime(data.get('birthday'), '%Y-%m-%d').date()
            if data.get('pic1024x768'):
                save_image(profile, data['pic1024x768'], social_account.provider)
        elif social_account.provider == 'google':
            profile.name = data.get('name', '')
            if data.get('picture'):
                save_image(profile, data['picture'], social_account.provider)
            if data.get('email'):
                profile.social_email = data['email']
        elif social_account.provider == 'facebook':
            profile.social_fb = f'https://www.facebook.com/profile.php?id={data["uid"]}'
            profile.name = data.get('name', '')
            if data.get('email'):
                profile.social_email = data['email']
        profile.save()


def save_image(model, url, provider='no'):
    fname = f"profile_{model.pk}_{provider}.jpg"
    cover = os.path.join(settings.MEDIA_ROOT, fname)
    with open(cover, 'wb+') as dest:
        preview = requests.get(url)
        dest.write(preview.content)
        model.image.save(fname, dest)


def youtube_get_id(url: str) -> str:
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
