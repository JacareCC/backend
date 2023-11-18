from django.contrib import admin
from django.urls import path
from jacare.views import helloWorld

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', helloWorld),
]
