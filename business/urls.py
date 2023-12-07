from django.contrib import admin
from django.urls import path
from business.views import new_registration_request, verify_review, get_business, get_specific_business, new_tier_level, edit_tier, delete_tier_level



urlpatterns = [
    path('register/', new_registration_request),
    path('review/verify/', verify_review),
    path('profile/', get_business),
    path('profile/<int:id>', get_specific_business),
    path('tier/new/', new_tier_level),
    path('tier/edit/<int:id>/', edit_tier),
    path('tier/remove/<int:id>/', delete_tier_level),
]