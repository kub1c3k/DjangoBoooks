from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from books import views  
from rest_framework.routers import DefaultRouter 



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("books.urls")),  
]

