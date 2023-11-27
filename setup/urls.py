from django.contrib import admin
from django.urls import path
from jacare.views import login_user, register_user, query_restaraurant, restaurant_detail, user_history, add_to_user_history, new_review 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user),
    path('register/', register_user),
    path('search/', query_restaraurant),
    path('restaurant/<int:id>/', restaurant_detail),
    path('user/history/', user_history),
    path('user/history/add/', add_to_user_history),
    path('submitreview/', new_review)
]
