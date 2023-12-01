from django.contrib import admin
from django.urls import path
from jacare.views import query_restaraurant, restaurant_detail, new_review, purchase_tier

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', query_restaraurant),
    path('restaurant/<int:id>/', restaurant_detail),
    path('review/new/', new_review),
    path('tier/purchase/', purchase_tier)
]
