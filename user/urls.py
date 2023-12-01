from django.contrib import admin
from django.urls import path
from user.views import user_history, add_to_user_history, get_all_user_tiers, get_user_saved_restaurants, change_user_saved_restaurants


urlpatterns = [
    path('history/', user_history),
    path('history/add/', add_to_user_history),
    path('tier/all/', get_all_user_tiers),
    path('favorites/all', get_user_saved_restaurants),
    path('favorites/add/', change_user_saved_restaurants),
    path('favorites/remove/', change_user_saved_restaurants),
]