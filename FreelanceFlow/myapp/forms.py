from django import forms
from django.contrib.auth.hashers import make_password

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Password'
            }
        )
    )


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Username'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Password'
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Confirm Password'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password before saving
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description',
                  'project_status', 'project_deadline', 'tags']
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Name'
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Description'
            }),
            'project_status': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Status'
            }),
            'project_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Deadline'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': '#tag'
            }),
        }


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description',
                  'project_status', 'project_deadline', 'tags']
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Project Name',
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Project Description',
                'rows': 4,
            }),
            'project_status': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'project_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
            }),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_name', 'tag_color']
        widgets = {
            'tag_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Tag Name',
            }),
            'tag_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'block w-full h-10 rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Tag Color',
            }),
        }


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description',
                  'task_status', 'task_priority', 'task_deadline']
        widgets = {
            'task_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Task Name',
            }),
            'task_description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Task Description',
            }),
            'task_status': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'task_priority': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'task_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Task Deadline',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)

    def clean_task_deadline(self):
        task_deadline = self.cleaned_data.get('task_deadline')
        if self.project and task_deadline > self.project.project_deadline:
            raise forms.ValidationError(
                "Task deadline cannot be later than the project's deadline.")
        return task_deadline


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description',
                  'task_status', 'task_priority', 'task_deadline']
        widgets = {
            'task_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Task Name',
            }),
            'task_description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Task Description',
            }),
            'task_status': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'task_priority': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'task_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Task Deadline',
            }),
        }

    def __init__(self, *args, **kwargs):
        # Expect the project instance to be passed
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    def clean_task_deadline(self):
        task_deadline = self.cleaned_data.get('task_deadline')
        if self.project and task_deadline and task_deadline > self.project.project_deadline:
            raise forms.ValidationError(
                "Task deadline cannot be later than the project's deadline."
            )
        return task_deadline
