import io
import json
import logging
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas

from .forms import *
from .forms import LoginForm, RegistrationForm
from .models import *
from .models import Project, Task, WeeklyReport

logger = logging.getLogger(__name__)


@login_required
def home_view(request):
    query = request.GET.get("q", "")
    project_status = request.GET.get("status", "")
    role = request.GET.get("role", "")

    projects = Project.objects.filter(
        Q(owner=request.user) | Q(viewers=request.user)
    ).distinct()

    if query:
        projects = projects.filter(
            Q(project_name__icontains=query) | Q(project_description__icontains=query)
        )

    if project_status:
        projects = projects.filter(project_status=project_status)

    if role == "owner":
        projects = projects.filter(owner=request.user)
    elif role == "viewer":
        projects = projects.filter(viewers=request.user)

    context = {
        "projects": projects,
        "query": query,
        "project_status": project_status,
        "role": role,
    }
    return render(request, "home.html", context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("myapp:home")
            else:
                form.add_error(None, "Invalid username or password.")
        else:
            print("Form errors:", form.errors)
    else:
        form = LoginForm()

    return render(request, "authentication/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("myapp:login")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()

    return render(request, "authentication/register.html", {"form": form})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner != request.user:
        return HttpResponseForbidden("You do not have permission to edit this project.")

    if request.method == "POST":
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect("myapp:home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditProjectForm(instance=project)
    context = {"form": form, "project": project}
    return render(request, "projects/edit_project.html", context)


@login_required
def create_project(request):
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()
            messages.success(request, "Project created successfully!")
            return redirect("myapp:home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreateProjectForm()

    context = {"form": form}
    return render(request, "projects/create_project.html", context)


@login_required
def delete_project(request):
    project_id = request.GET.get("id")
    if not project_id:
        messages.error(request, "Project ID is missing.")
        return redirect("myapp:home")

    project = get_object_or_404(Project, project_id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden(
            "You don't have permission to delete this project."
        )

    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect("myapp:home")


@login_required
def project_details(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user != project.owner and request.user not in project.viewers.all():
        return render(request, "403.html", status=403)

    query = request.GET.get("q", "")
    task_status = request.GET.get("status", "")
    task_priority = request.GET.get("priority", "")

    tasks = project.tasks.all()
    if query:
        tasks = tasks.filter(
            Q(task_name__icontains=query) | Q(task_description__icontains=query)
        )
    if task_status:
        tasks = tasks.filter(task_status=task_status)
    if task_priority:
        tasks = tasks.filter(task_priority=task_priority)
    users = project.viewers.all()
    context = {
        "project": project,
        "users": users,
        "tasks": tasks,
        "query": query,
        "task_status": task_status,
        "task_priority": task_priority,
    }
    return render(request, "projects/project_details.html", context)


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = CreateTaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect("myapp:project_details", pk=project_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CreateTaskForm(project=project)

    return render(request, "tasks/create_task.html", {"form": form, "project": project})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = task.project

    if request.user != project.owner and request.user not in project.viewers.all():
        messages.error(request, "You do not have permission to edit this task.")
        return redirect("myapp:project_details", pk=project.project_id)

    if request.method == "POST":
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("myapp:project_details", pk=project.project_id)
        else:
            messages.error(
                request, "There was an error updating the task. Please try again."
            )
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
    task = get_object_or_404(Task, task_id=task_id)

    if task.project.owner != request.user:
        return HttpResponseForbidden("You do not have permission to delete this task.")

    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect("myapp:project_details", pk=task.project.project_id)


@login_required
def add_user_to_project(request, project_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email", "").strip()

            if not email:
                return JsonResponse({"error": "Email is required."}, status=400)

            users = User.objects.filter(email__iexact=email)

            if not users.exists():
                return JsonResponse({"error": "User not found."}, status=404)

            user = users.first()

            project = get_object_or_404(Project, project_id=project_id)

            project.viewers.add(user)

            return JsonResponse(
                {
                    "success": True,
                    "message": f"User {user.username} added successfully.",
                },
                status=200,
            )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
@login_required
def update_task_status(request, task_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status")

            if new_status not in dict(Task.TASK_STATUS_CHOICES):
                return JsonResponse({"error": "Invalid status"}, status=400)

            task = get_object_or_404(Task, pk=task_id)
            task.task_status = new_status
            task.save()
            return JsonResponse({"message": "Task status updated successfully!"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def delete_task(request, task_id):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            task = get_object_or_404(Task, pk=task_id)
            task.delete()
            return JsonResponse({"message": "Task deleted successfully!"})
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=405)


from django.core.management import call_command


@login_required
def generate_report_view(request):
    try:
        call_command("generate_reports")
    except Exception as e:
        return HttpResponse(f"Error generating reports: {str(e)}", status=500)

    reports = WeeklyReport.objects.filter(project__owner=request.user).order_by(
        "-end_date"
    )

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, f"Weekly Report for {request.user.username}")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(100, 780, f"Generated on: {now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = 750
    if reports.exists():
        for report in reports:
            project = report.project
            y -= 40
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(100, y, f"Project: {project.project_name}")
            pdf.setFont("Helvetica", 10)
            y -= 20
            pdf.drawString(120, y, f"Completed Tasks: {report.completed_tasks_count}")
            y -= 20
            pdf.drawString(
                120, y, f"Completion Percentage: {report.completion_percentage:.2f}%"
            )
            y -= 20
            pdf.drawString(
                120, y, f"Start Date: {report.start_date.strftime('%Y-%m-%d')}"
            )
            pdf.drawString(
                120, y - 20, f"End Date: {report.end_date.strftime('%Y-%m-%d')}"
            )
            y -= 40

            if y < 100:
                pdf.showPage()
                y = 750
    else:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, y, "No reports available.")

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        f"attachment; filename=Weekly_Report_{request.user.username}.pdf"
    )
    return response
