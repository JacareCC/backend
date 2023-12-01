from django.contrib import admin
from django.urls import path, include
from jacare.views import query_restaraurant, restaurant_detail, new_review, purchase_tier, login_user, register_user

urlpatterns = [
    path('login/', login_user),
    path('register/', register_user),
    path('admin/', admin.site.urls),
    path('search/', query_restaraurant),
    path('restaurant/<int:id>/', restaurant_detail),
    path('review/new/', new_review),
    path('tier/purchase/', purchase_tier),
    path('user/', include('user.urls')),
    path('business/', include('business.urls'))
]
