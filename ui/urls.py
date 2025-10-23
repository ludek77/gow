from django.urls import re_path

from ui.views import ui_views, user_views, game_views, city_views, country_views, unit_views, field_views

urlpatterns = [
    re_path(r'^$', ui_views.index, name='index'),
    re_path(r'^field_dialog/', ui_views.field_dialog, name='field_dialog'),
    re_path(r'^new_field_dialog/', ui_views.new_field_dialog, name='new_field_dialog'),
    re_path(r'^game_dialog/', ui_views.game_dialog, name='game_dialog'),
    
    re_path(r'^logout/', user_views.logout_rest, name='logout'),
    re_path(r'^login/', user_views.login_rest, name='login'),
    
    re_path(r'^game_list/', game_views.game_list_rest, name='game_list'),
    re_path(r'^game_select/', game_views.game_select_rest, name='game_select'),
    re_path(r'^game_setup/', game_views.game_setup_rest, name='game_setup'),
    re_path(r'^game_start/', game_views.game_start_rest, name='game_start'),
    re_path(r'^turn_previous/', game_views.turn_previous_rest, name='turn_previous'),
    re_path(r'^turn_next/', game_views.turn_next_rest, name='turn_next'),
    
    re_path(r'^country_setup/', country_views.country_setup_rest, name='country_setup'),
    
    re_path(r'^field_add/', field_views.field_add_rest, name='field_add'),
    re_path(r'^field_delete/', field_views.field_delete_rest, name='field_delete'),
    re_path(r'^path_add/', field_views.path_add_rest, name='path_add'),
    re_path(r'^path_delete/', field_views.path_delete_rest, name='path_delete'),
    
    re_path(r'^city_get/', city_views.city_get_rest, name='city_get'),
    
    re_path(r'^unit_get/', unit_views.unit_get_rest, name='unit_get'),
    re_path(r'^unit_command/', unit_views.unit_command_rest, name='unit_command'),
    re_path(r'^city_command/', unit_views.city_command_rest, name='city_command'),
]