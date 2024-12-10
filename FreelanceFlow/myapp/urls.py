from django.urls import path , include
from . import views
from django.contrib import admin
from django.views.generic.base import TemplateView  # new

app_name = 'myapp'  # here for namespacing of urls.

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),  # new
]