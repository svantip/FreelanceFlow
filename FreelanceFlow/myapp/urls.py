from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(),
         name='logout'),  # Logout page
    path('register/', views.register_view, name='register'),  # Register page
]
