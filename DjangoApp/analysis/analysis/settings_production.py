from .settings import *  # noqa


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'analysis',
        'USER': 'python',
        'PASSWORD': 'python',
        'HOST': 'localhost',
    }
}

#STATIC_ROOT = '/home/mnu/public_html/tutorial/static/'
#STATIC_ROOT = '/home/mizu_masaru/masaruOfficeGit/django/DjangoApp/analysis/static'
