from django.contrib import admin
from django.urls import path
from user.views import login_user, register_user, user_history, add_to_user_history, get_all_user_tiers, get_user_saved_restaurants, change_user_saved_restaurants


urlpatterns = [
    path('login/', login_user),
    path('register/', register_user),
    path('user/history/', user_history),
    path('user/history/add/', add_to_user_history),
    path('user/tier/all/', get_all_user_tiers),
    path('user/favorites/all', get_user_saved_restaurants),
    path('user/favorites/add/', change_user_saved_restaurants),
    path('user/favorites/remove/', change_user_saved_restaurants),
]