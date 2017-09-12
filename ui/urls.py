from django.conf.urls import url

from ui.views import ui_views, user_views, game_views, city_views, country_views, unit_views, field_views

urlpatterns = [
    url(r'^$', ui_views.index, name='index'),
    url(r'^unit_dialog/', ui_views.unit_dialog, name='unit_dialog'),
    url(r'^city_dialog/', ui_views.city_dialog, name='city_dialog'),
    url(r'^field_dialog/', ui_views.field_dialog, name='field_dialog'),
    
    url(r'^logout/', user_views.logout_rest, name='logout'),
    url(r'^login/', user_views.login_rest, name='login'),
    
    url(r'^game_list/', game_views.game_list_rest, name='game_list'),
    url(r'^game_select/', game_views.game_select_rest, name='game_select'),
    url(r'^game_setup/', game_views.game_setup_rest, name='game_setup'),
    
    url(r'^country_setup/', country_views.country_setup_rest, name='country_setup'),
    
    url(r'^field_add/', field_views.field_add_rest, name='field_add'),
    url(r'^field_delete/', field_views.field_delete_rest, name='field_delete'),
    url(r'^path_add/', field_views.path_add_rest, name='path_add'),
    url(r'^path_delete/', field_views.path_delete_rest, name='path_delete'),
    
    url(r'^city_get/', city_views.city_get_rest, name='city_get'),
    
    url(r'^unit_get/', unit_views.unit_get_rest, name='unit_get'),
    url(r'^unit_command/', unit_views.unit_command_rest, name='unit_command'),
]