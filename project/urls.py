from django.conf.urls import include, url
from django.contrib import admin

from ui.views import index

urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),
]
