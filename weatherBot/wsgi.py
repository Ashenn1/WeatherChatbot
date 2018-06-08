"""
WSGI config for weatherbot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys


from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

project_home = u'C:\Users\Soha Samad\Desktop\College\year 3\Second Semester\SWE for PC-Human Interaction\ChatBotCode\Bot\weatherBot'

if project_home not in sys.path:
    sys.path.append(project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherBot.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)