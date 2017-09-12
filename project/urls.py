from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^ui/', include('ui.urls')),
    url(r'^admin/', admin.site.urls),
]
