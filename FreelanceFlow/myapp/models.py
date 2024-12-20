from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    tag_name = models.CharField(max_length=100, unique=True)
    tag_color = models.CharField(max_length=7, default="#ADB2BE")

    def __str__(self):
        return self.tag_name


class Project(models.Model):
    PROJECT_STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    project_name = models.CharField(max_length=200, unique=True)
    project_description = models.TextField(blank=True)
    project_status = models.CharField(
        max_length=20, choices=PROJECT_STATUS_CHOICES)
    project_deadline = models.DateTimeField()
    project_created = models.DateTimeField(auto_now_add=True)
    project_updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects")

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
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(blank=True)
    task_status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES)
    task_priority = models.CharField(
        max_length=20, choices=TASK_PRIORITY_CHOICES)
    task_deadline = models.DateTimeField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks")
    task_created = models.DateTimeField(auto_now_add=True)
    task_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name
