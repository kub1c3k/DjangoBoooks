from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from books import views  
from user import views as user_view
from django.contrib.auth import views as auth



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("books.urls")),  
    path('', include('user.urls')),
    path('login/', user_view.Login, name ='login'),
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    path('register/', user_view.register, name ='register'),
]

