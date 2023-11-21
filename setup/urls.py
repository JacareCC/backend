from django.contrib import admin
from django.urls import path
from jacare.views import login_user, register_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user),
    path('register/', register_user)
]
