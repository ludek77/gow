from django.conf.urls import url

from ui.views import views, user_views, game_views

urlpatterns = [
    url(r'^$', views.index),
    
    url(r'^logout/', user_views.logout_rest),
    url(r'^login/', user_views.login_rest),
    
    url(r'^game_list/', game_views.game_list_rest),
    url(r'^game_select/', game_views.game_select_rest),
    url(r'^game_setup/', game_views.game_setup_rest),
    
    url(r'^country_setup/', views.country_setup_rest),
]