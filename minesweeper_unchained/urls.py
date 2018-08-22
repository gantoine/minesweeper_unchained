from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('sweeper.urls')),
    path('admin/', admin.site.urls),
]
