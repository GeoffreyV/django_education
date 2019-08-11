### local_settings.py
### environment-specific settings
### example with a development environment

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'sql_mode': 'traditional',},
            'NAME': 'django_education',
        'USER': 'django',
        'PASSWORD': 'd40;B64!p17',
        'HOST': 'www.costadoat.fr',
        'PORT': '3306',
    }
}

ALLOWED_HOSTS = ['127.0.0.1','192.168.0.16','78.192.222.66','www.costadoat.fr']
