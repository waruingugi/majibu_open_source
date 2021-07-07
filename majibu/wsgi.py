"""
WSGI config for majibu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os  # noqa
from django.core.wsgi import get_wsgi_application  # noqa
from dj_static import Cling  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'majibu.settings')

application = Cling(get_wsgi_application())
