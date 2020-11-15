from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect

from api import models
from front import forms, methods


class WriterView(View):
    def get(self, request, pk=None):
        if not request.user.is_authenticated:
            request.session['message'] = 'Вы должны войти, чтобы редактировать статью'
            return redirect('/auth/login/')
        if pk:
            article = models.News.objects.filter(pk=pk, author_profile=request.user.profile).first()
            if not article:
                request.session['message'] = 'Статья не найдена или это не ваша статья'
                return redirect(f'/profile-{request.user.profile.pk}')
        else:
            article = models.News()
        context = {
            'form': forms.NewsForm(instance=article),
            'section_list': models.NewsSection.objects.filter(active=True),
            'footer_extend': '<script src="https://cdn.tiny.cloud/1/lh4zfqr7jd1gvgc880bkn5z61dxah88ogs92zje69rgpmk0b/tinymce/5/tinymce.min.js" referrerpolicy="origin"/></script>'
                             "<script>tinymce.init({"
                             "selector:'#article-text-id',"
                             "menubar: false,"
                             'plugins: "code lists link image emoticons",'
                             "toolbar:  'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | emoticons | removeformat | forecolor backcolor | link image | code',"
                             # "tinydrive_token_provider: '',"
                             "});</script>"
        }
        return render(request, 'writer.html', context)

    def post(self, request, pk=None):
        if not request.user.is_authenticated:
            request.session['message'] = 'Вы должны войти, чтобы редактировать статью'
            return redirect('/auth/login/')
        if pk:
            article = models.News.objects.filter(pk=pk, author_profile=request.user.profile).first()
            if not article:
                request.session['message'] = 'Статья не найдена или это не ваша статья'
                return redirect('/')
            form = forms.NewsForm(request.POST, request.FILES, instance=article)
        else:
            form = forms.NewsForm(request.POST, request.FILES)
        form.data = form.data.copy()
        if form.data.get('section') == '---':
            del form.data['section']
        if 'date' in form.data and not form.data.get('date'):
            del form.data['date']
        if form.is_valid():
            form = form.save(commit=False)
            form.author_profile = request.user.profile
            if not request.user.is_staff:
                form.section = None
            form.save()
        return redirect(f'/profile-{request.user.profile.pk}')


class ProfileView(View):
    def get(self, request, pk=None):
        if not request.user.is_authenticated:
            request.session['message'] = 'Вы должны войти, чтобы увидеть профиль пользователя'
            return redirect('/auth/login/')
        if pk:
            profile = models.Profile.objects.filter(pk=pk).first()
            if not profile:
                request.session['message'] = 'Пользователь не найден'
                profile = request.user.profile
        else:
            profile = request.user.profile
        profile_html = render_to_string('include/profile.html', {
            'item': profile
        }, request)
        context = {
            'profile_html': profile_html,
            'profile': profile
        }
        return render(request, 'profile.html', context)


class IndexView(View):
    def get(self, request):
        context = {
            'news': models.News.objects.filter(active=True, date__gte=timezone.now())[:7],
            'main': models.Main.get_solo(),
            'title': models.Main.get_solo().title
        }
        if 'message' in request.session:
            del request.session['message']
        return render(request, 'index.html', context)


class AccountView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/auth/login/')
        profile, created = models.Profile.objects.get_or_create(user=request.user)
        if created:
            methods.fill_social(profile)
        account = render_to_string('include/account.html', {
            'item': profile
        }, request)
        context = {
            'account': account,
        }
        return render(request, 'account.html', context)

    def post(self, request):
        profile = request.user.profile
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('/account')


class CommandView(View):
    def get(self, request):
        command = render_to_string('include/command.html', {
            'command': models.Profile.objects.filter(position__lt=90, active=True).order_by('position')
        })
        context = {
            'command': command,
        }
        return render(request, 'command.html', context)


class NewsSectionView(View):
    def get(self, request, pk):
        news_section = models.NewsSection.objects.filter(pk=pk).first()
        if not news_section:
            news_section = models.NewsSection.objects.first()
        try:
            newssection = render_to_string('include/newssection.html', {
                'newssection': news_section,
                'newssection_all': models.NewsSection.objects.filter(
                    active=True, news__active=True, date__gte=timezone.now()
                ).distinct()
            })
        except Exception as Ex:
            print(Ex)
            return redirect('/')
        context = {
            'newssection': newssection,
        }
        return render(request, 'newssection.html', context)


class ArticleView(View):
    def get(self, request, pk):
        try:
            article = models.News.objects.get(pk=pk, date__gte=timezone.now())
            article_html = render_to_string('include/article.html', {
                'article': article,
                'newssection_all': models.NewsSection.objects.filter(active=True, news__active=True).distinct()
            }, request)
        except Exception as Ex:
            request.session['message'] = 'Статья не найдена'
            print(Ex)
            return redirect('/news')
        context = {
            'article': article_html,
            'title': article.title
        }
        return render(request, 'article.html', context)


class StaticView(View):
    def get(self, request):
        path = request.path[1:] + '.html'
        context = {
            'main': models.Main.get_solo(),
            'title': models.Main.get_solo().title
        }
        try:
            return render(request, path, context)
        except Exception as Ex:
            print(Ex)
            return redirect('/')
