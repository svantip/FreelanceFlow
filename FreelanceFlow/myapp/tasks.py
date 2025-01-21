from celery import shared_task
from datetime import timedelta
from django.db.models import Count
from django.core.cache import cache
from django.utils.timezone import now
from .models import Project, Task, WeeklyReport


@shared_task
def generate_weekly_report():
    end_date = now()
    start_date = end_date - timedelta(days=7)

    start_date = start_date.astimezone()
    end_date = end_date.astimezone()

    tasks = Task.objects.filter(
        task_status="completed",
        task_updated__range=[start_date, end_date]
    ).values('project_id', 'project__project_name').annotate(
        completed_tasks_count=Count('task_id')
    )

    for task_group in tasks:
        project = Project.objects.get(pk=task_group['project_id'])
        WeeklyReport.objects.update_or_create(
            project=project,
            start_date=start_date,
            end_date=end_date,
            defaults={
                "completed_tasks_count": task_group['completed_tasks_count'],
            },
        )

    # Cache the generated report data
    cache_key = f"weekly_report_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"
    cache.set(cache_key, list(tasks), timeout=7 * 24 * 60 * 60)
