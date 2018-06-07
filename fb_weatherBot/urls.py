
from django.conf.urls import include, url
from .views import weatherBotView
urlpatterns = [
                   url(r'^672150ab61db99740d67878200287e76e7ae2bd17089a89aff/?$', weatherBotView.as_view())
               ]