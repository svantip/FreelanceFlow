import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from .models import Project
from .forms import *
from django.core.exceptions import ValidationError


from .forms import LoginForm, RegistrationForm


@login_required
def home_view(request):
    user = request.user
    # Fetch projects where the user is the owner or a viewer
    projects = Project.objects.filter(
        owner=user) | Project.objects.filter(viewers=user)
    context = {"projects": projects}
    return render(request, "home.html", context)


def login_view(request):
    """
    Handle user login functionality.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('myapp:home')
            else:
                # Add a non-field error for invalid credentials
                form.add_error(None, "Invalid username or password.")
        else:
            # Log form errors for debugging purposes
            print("Form errors:", form.errors)
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def register_view(request):
    """
    Handle user registration functionality.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(
                request, "Registration successful! You can now log in."
            )
            # Redirect to login after registration
            return redirect('myapp:login')
        else:
            print(form.errors)  # Debugging: Print errors in the console
    else:
        form = RegistrationForm()

    return render(request, 'authentication/register.html', {'form': form})


@login_required
def edit_project(request, pk):
    """
    Handle editing of a project by its owner.
    Only the owner of the project can edit it.
    """
    project = get_object_or_404(Project, pk=pk)

    # Ensure the logged-in user is the owner of the project
    if project.owner != request.user:
        return HttpResponseForbidden("You do not have permission to edit this project.")

    if request.method == "POST":
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            # Redirect to the home page after saving
            return redirect('myapp:home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditProjectForm(instance=project)
    context = {"form": form, "project": project}
    return render(request, "projects/edit_project.html", context)


@login_required
def create_project(request):
    """
    Handle creating a new project by the logged-in user.
    """
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            # Save the form with the logged-in user as the owner
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()  # Save many-to-many data (tags)
            messages.success(request, "Project created successfully!")
            return redirect('myapp:home')  # Redirect to the home page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreateProjectForm()

    context = {"form": form}
    return render(request, "projects/create_project.html", context)


@login_required
def delete_project(request):
    # Get the project_id from the query string
    project_id = request.GET.get('id')
    if not project_id:
        messages.error(request, "Project ID is missing.")
        return redirect('myapp:home')

    # Query using project_id (the correct field name)
    project = get_object_or_404(Project, project_id=project_id)

    # Ensure only the owner can delete the project
    if project.owner != request.user:
        return HttpResponseForbidden("You don't have permission to delete this project.")

    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect('myapp:home')


@login_required
def project_details(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Ensure the user has access to the project
    if request.user != project.owner and request.user not in project.viewers.all():
        # Return 403 forbidden page if unauthorized
        return render(request, "403.html", status=403)

    tasks = project.tasks.all()
    users = project.viewers.all()  # Users who have access

    context = {
        'project': project,
        'tasks': tasks,
        'users': users,
    }
    return render(request, 'projects/project_details.html', context)


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = CreateTaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project  # Ensure this is set before saving
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect('myapp:project_details', pk=project_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreateTaskForm(project=project)

    return render(request, 'tasks/create_task.html', {'form': form, 'project': project})


@login_required
def edit_task(request, task_id):
    """
    View to edit an existing task.
    """
    task = get_object_or_404(Task, pk=task_id)
    project = task.project

    # Check if the user has permission to edit tasks in this project
    if request.user != project.owner and request.user not in project.viewers.all():
        messages.error(
            request, "You do not have permission to edit this task.")
        return redirect("myapp:project_details", pk=project.project_id)

    if request.method == "POST":
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("myapp:project_details", pk=project.project_id)
        else:
            messages.error(
                request, "There was an error updating the task. Please try again.")
    else:
        form = EditTaskForm(instance=task)

    context = {
        "form": form,
        "task": task,
        "project": project,
    }
    return render(request, "projects/edit_task.html", context)


@login_required
def delete_task(request, task_id):
    """
    Handle the deletion of a task.
    Only the owner of the associated project can delete the task.
    """
    # Fetch the task by its ID
    task = get_object_or_404(Task, task_id=task_id)

    # Check if the logged-in user is the owner of the associated project
    if task.project.owner != request.user:
        return HttpResponseForbidden("You do not have permission to delete this task.")

    # Delete the task
    task.delete()
    messages.success(request, "Task deleted successfully!")
    # Redirect to the project's details page or any other appropriate page
    return redirect('myapp:project_details', pk=task.project.project_id)


@login_required
def add_user_to_project(request, project_id):
    if request.method == "POST":
        try:
            # Parse JSON body
            data = json.loads(request.body)
            # Strip leading/trailing spaces
            email = data.get("email", "").strip()
            print(f"Email received: {email}")

            if not email:
                return JsonResponse({"error": "Email is required."}, status=400)

            # Debug: Check if email exists in the database
            users = User.objects.filter(email__iexact=email)
            print(f"Users found: {users}")

            if not users.exists():
                return JsonResponse({"error": "User not found."}, status=404)

            user = users.first()
            print(f"User selected: {user}")

            # Use correct field for project lookup
            project = get_object_or_404(Project, project_id=project_id)
            print(f"Project: {project}")

            # Add user to project viewers
            project.viewers.add(user)
            return JsonResponse({"success": True, "message": f"User {user.username} added successfully."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
