import logging
from celery import shared_task
from datetime import timedelta
from django.db.models import Count
from django.core.cache import cache
from django.utils.timezone import now
from .models import Project, Task, WeeklyReport
from django.db.models import Q

logger = logging.getLogger(__name__)

@shared_task
def generate_weekly_report():
    logger.info("Starting weekly report generation task...")

    cache.delete("latest_weekly_reports")
    cache.delete_pattern("weekly_report_*")
    logger.info("Cache cleared for weekly reports.")

    end_date = now()
    start_date = end_date - timedelta(days=7)

    start_date = start_date.astimezone()
    end_date = end_date.astimezone()

    completed_tasks = Task.objects.filter(
        task_status="completed",
        task_updated__range=[start_date, end_date]
    ).values('project_id', 'project__project_name').annotate(
        completed_tasks_count=Count('task_id')
    )

    total_tasks = Task.objects.filter(
        task_updated__range=[start_date, end_date]
    ).values('project_id').annotate(
        total_tasks_count=Count('task_id')
    )

    total_tasks_lookup = {task['project_id']: task['total_tasks_count'] for task in total_tasks}

    latest_reports = []
    for task_group in completed_tasks:
        project_id = task_group['project_id']
        project = Project.objects.get(pk=project_id)

        total_tasks_count = total_tasks_lookup.get(project_id, 0)
        completed_tasks_count = task_group['completed_tasks_count']

        completion_percentage = (
            completed_tasks_count / total_tasks_count) * 100 if total_tasks_count > 0 else 0

        report, created = WeeklyReport.objects.update_or_create(
            project=project,
            start_date=start_date,
            end_date=end_date,
            defaults={
                "completed_tasks_count": completed_tasks_count,
                "completion_percentage": completion_percentage,
            },
        )

        # Append the newly created/updated report to the list for caching
        latest_reports.append({
            "project_name": project.project_name,
            "completed_tasks_count": completed_tasks_count,
            "completion_percentage": completion_percentage,
            "start_date": start_date,
            "end_date": end_date,
        })

    # Cache the newly generated reports
    cache_key = "latest_weekly_reports"
    cache.set(cache_key, latest_reports, timeout=7 * 24 * 60 * 60)

    logger.info("Weekly report generation task completed.")