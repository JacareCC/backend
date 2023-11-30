from django.contrib import admin
from django.urls import path
from jacare.views import login_user, register_user, query_restaraurant, restaurant_detail, user_history, add_to_user_history, new_review, change_user_saved_restaurants, get_user_saved_restaurants, new_registration_request, verify_review, get_reviews, new_tier_level, get_all_tiers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user),
    path('register/', register_user),
    path('search/', query_restaraurant),
    path('restaurant/<int:id>/', restaurant_detail),
    path('user/history/', user_history),
    path('user/history/add/', add_to_user_history),
    path('submitreview/', new_review),
    path('user/favorites/', get_user_saved_restaurants),
    path('user/favorites/add/', change_user_saved_restaurants),
    path('user/favorites/remove/', change_user_saved_restaurants),
    path('business/register/', new_registration_request),
    path('review/verify/', verify_review),
    path('business/reviews/', get_reviews),
    path('tier/new/', new_tier_level),
    path('tier/all/', get_all_tiers)
]
