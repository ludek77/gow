from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout/', views.logout_view),
    url(r'^login/', views.login_view),
]