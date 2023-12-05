from django.contrib import admin
from django.urls import path
from user.views import get_all_user_tiers, get_user_saved_restaurants, change_user_saved_restaurants, get_profile, update_user


urlpatterns = [
    path('profile/', get_profile),
    path('edit/', update_user),
    path('tier/all/', get_all_user_tiers),
    path('favorites/all', get_user_saved_restaurants),
    path('favorites/add/', change_user_saved_restaurants),
    path('favorites/remove/', change_user_saved_restaurants),
]