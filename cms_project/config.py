import os


DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',  # Use PostgreSQL backend

        'NAME': os.environ.get('POSTGRES_DB', 'cms_db'),  # Database name

        'USER': os.environ.get('POSTGRES_USER', 'mahi'),  # Database user

        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'mahi123'),  # Database password

        'HOST': os.environ.get('POSTGRES_HOST', 'db'),  # Database host

        'PORT': os.environ.get('POSTGRES_PORT', '5432'),  # Database port

    }

}