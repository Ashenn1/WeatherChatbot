
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^fb_weatherBot/', include('fb_weatherBot.urls')),
]
