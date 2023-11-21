from django.contrib import admin
from django.urls import path
from jacare.views import login_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', login_user),
]
