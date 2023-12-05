from django.contrib import admin
from django.urls import path
from business.views import new_registration_request, verify_review, get_reviews, new_tier_level, edit_tier, delete_tier_level



urlpatterns = [
    path('business/register/', new_registration_request),
    path('business/review/verify/', verify_review),
    path('business/review/all/', get_reviews),
    path('business/tier/new/', new_tier_level),
    path('business/tier/edit/<int:id>/', edit_tier),
    path('business/tier/remove/<int:id>/', delete_tier_level),
]