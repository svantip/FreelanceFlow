from celery import shared_task
from datetime import timedelta
from django.db.models import Count
from django.core.cache import cache
from django.utils.timezone import now
from .models import Task, WeeklyReport


@shared_task
def generate_weekly_report():
    end_date = now()
    start_date = end_date - timedelta(days=7)

    # Ensure dates are timezone-aware
    start_date = start_date.astimezone()
    end_date = end_date.astimezone()

    # Remove old reports for the same period
    WeeklyReport.objects.filter(
        start_date=start_date, end_date=end_date).delete()

    # Fetch completed tasks and group by project
    tasks = Task.objects.filter(
        task_status="completed",
        task_updated__range=[start_date, end_date]
    ).values('project_id', 'project__project_name').annotate(completed_tasks_count=Count('task_id'))

    # Save the report data in the database
    for task_group in tasks:
        WeeklyReport.objects.create(
            project_id=task_group['project_id'],
            completed_tasks_count=task_group['completed_tasks_count'],
            start_date=start_date,
            end_date=end_date,
        )

    # Cache the generated report data
    cache_key = f"weekly_report_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"
    cache.set(cache_key, list(tasks), timeout=7 * 24 * 60 * 60)
