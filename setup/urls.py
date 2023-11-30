from django.contrib import admin
from django.urls import path
from jacare.views import login_user, register_user, query_restaraurant, restaurant_detail, user_history, add_to_user_history, new_review, change_user_saved_restaurants, get_user_saved_restaurants, new_registration_request, verify_review, get_reviews, new_tier_level, get_all_tiers, purchase_tier, get_all_user_tiers, edit_tier, delete_tier_level

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user),
    path('register/', register_user),
    path('search/', query_restaraurant),
    path('restaurant/<int:id>/', restaurant_detail),
    path('user/history/', user_history),
    path('user/history/add/', add_to_user_history),
    path('user/tier/all/', get_all_user_tiers),
    path('submitreview/', new_review),
    path('user/favorites/', get_user_saved_restaurants),
    path('user/favorites/add/', change_user_saved_restaurants),
    path('user/favorites/remove/', change_user_saved_restaurants),
    path('business/register/', new_registration_request),
    path('business/review/verify/', verify_review),
    path('business/reviews/', get_reviews),
    path('business/tier/new/', new_tier_level),
    path('business/tier/edit/<int:id>/', edit_tier),
    path('business/tier/remove/<int:id>/', delete_tier_level),
    path('tier/all/', get_all_tiers),
    path('tier/purchase/', purchase_tier)
]
