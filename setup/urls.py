from django.contrib import admin
from django.urls import path, include
from jacare.views import query_restaraurant, new_review, purchase_tier, login_user, register_user, check_in

urlpatterns = [
    path('login/', login_user),
    path('register/', register_user),
    path('admin/', admin.site.urls),
    path('search/', query_restaraurant),
    path('review/new/', new_review),
    path('checkin/', check_in),
    path('tier/purchase/', purchase_tier),
    path('user/', include('user.urls')),
    path('business/', include('business.urls'))
]

## review to add we would use post and to get the review we would have to use get 
