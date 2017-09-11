from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    
    url(r'^logout/', views.logout_rest),
    url(r'^login/', views.login_rest),
    
    url(r'^game_list/', views.game_list_rest),
    url(r'^game_select/', views.game_select_rest),
    url(r'^game_setup/', views.game_setup_rest),
    
    url(r'^country_setup/', views.country_setup_rest),
]