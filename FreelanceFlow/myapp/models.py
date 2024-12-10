from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
  # Import Django's built-in User model
from django.db import models

class User(models.Model):
    ID_User = models.AutoField(primary_key=True)
    Username =models.CharField(max_length=100, unique=True)
    Email = models.EmailField(max_length=100, unique=True)
    Password = models.CharField(max_length=100)
    User_created=models.DateTimeField(auto_now_add=True)

# Tag model
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)  # Primary Key
    tag_name = models.CharField(max_length=100, unique=True)  # Tag Name
    tag_color = models.CharField(max_length=7, default="#ADB2BE")  # Default color

    def __str__(self):
        return self.tag_name


# Project model
class Project(models.Model):
    PROJECT_STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    id_project = models.AutoField(primary_key=True)  # Primary Key
    project_name = models.CharField(max_length=200, unique=True)  # Unique Project Name
    project_description = models.TextField(blank=True)  # Project Description
    project_status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES)  # Status Choices
    project_deadline = models.DateTimeField()  # Deadline
    project_created = models.DateTimeField(auto_now_add=True)  # Auto-set creation time
    project_updated = models.DateTimeField(auto_now=True)  # Auto-set update time
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)  # Many-to-Many relationship with Tags
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")  # Foreign Key to User

    def __str__(self):
        return self.project_name
   
class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    TASK_PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    id_task = models.AutoField(primary_key=True)  # Primary Key
    task_name = models.CharField(max_length=200)  # Task Name
    task_description = models.TextField(blank=True)  # Task Description
    task_status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES)  # Status Choices
    task_priority = models.CharField(max_length=20, choices=TASK_PRIORITY_CHOICES)  # Priority Choices
    task_deadline = models.DateTimeField()  # Task Deadline
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")  # Foreign Key to Project
    task_created = models.DateTimeField(auto_now_add=True)  # Auto-set creation time
    task_updated = models.DateTimeField(auto_now=True)  # Auto-set update time

    def __str__(self):
        return self.task_name