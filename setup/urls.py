from django.contrib import admin
from django.urls import path
from jacare.views import authenticate_firebase_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', authenticate_firebase_user),
]
