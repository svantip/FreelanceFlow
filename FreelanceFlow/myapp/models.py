import re
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class Tag(models.Model):
    tag_id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(max_length=100, unique=True)
    tag_color = models.CharField(max_length=7, default="#ADB2BE")

    def __str__(self):
        return self.tag_name

    def clean(self):
        if not re.match(r'^#[A-Fa-f0-9]{6}$', self.tag_color):
            raise ValueError("tag_color must be a valid hex color code.")


class Project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    PROJECT_STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),         # (database_value, display_name)
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
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,  # Allows the field to accept NULL in the database
        blank=True,  # Makes it optional in forms
    )
    viewers = models.ManyToManyField(
        User, related_name="viewable_project", blank=True)

    def __str__(self):
        return self.project_name

    @classmethod
    def get_projects_by_status(cls, status):
        return cls.objects.filter(project_status=status)

    def calculate_progress(self):
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter(task_status="completed").count()
        return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    def clean(self):
        from django.utils.timezone import now
        if self.project_deadline < now():
            raise ValueError("Project deadline must be in the future.")


class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    TASK_STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),         # (database_value, display_name)
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
        max_length=20, choices=TASK_PRIORITY_CHOICES
    )
    task_deadline = models.DateTimeField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks"
    )
    task_created = models.DateTimeField(auto_now_add=True)
    task_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name

    @classmethod
    def get_tasks_by_priority(cls, priority):
        return cls.objects.filter(task_priority=priority)
