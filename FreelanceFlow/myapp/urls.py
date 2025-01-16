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
    path('projects/<int:pk>/edit/', views.edit_project,
         name='edit_project'),  # Edit project
    path('projects/create/', views.create_project,
         name='create_project'),  # Create project
    path('projects/delete/', views.delete_project,
         name='delete_project'),  # Delete project
    path('projects/<int:pk>/', views.project_details,
         name='project_details'),  # Project details
    path('tasks/create/<int:project_id>/', views.create_task,
         name='create_task'),  # Create task,
    path('tasks/<int:pk>/edit', views.edit_task, name='edit_task'),  # Edit task
    path('tasks/delete/', views.delete_task,
         name="delete_task"),  # Delete task
    path('projects/<int:project_id>/add-user/',
         views.add_user_to_project, name='add_user_to_project'),
     path('update_task_status/<int:task_id>/', views.update_task_status, 
          name='update_task_status'),
    path('delete_task/<int:task_id>/',
          views.delete_task, name='delete_task'),


]
