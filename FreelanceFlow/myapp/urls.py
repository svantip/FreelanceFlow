from django.urls import path , include
from . import views
from django.contrib import admin
from django.views.generic.base import TemplateView  # new
from .views import *
app_name = 'myapp'  # here for namespacing of urls.

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

]