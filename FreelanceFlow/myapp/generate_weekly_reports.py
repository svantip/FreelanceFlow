from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.db.models import Count
from myapp.models import Task, WeeklyReport


class Command(BaseCommand):
    help = "Generate weekly task completion reports."

    def handle(self, *args, **kwargs):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Fetch completed tasks and group by project
        tasks = Task.objects.filter(
            task_status="completed",
            task_updated__range=[start_date, end_date]
        ).values('project').annotate(completed_tasks_count=Count('id'))

        # Save the report data
        for task_group in tasks:
            WeeklyReport.objects.update_or_create(
                project_id=task_group['project'],
                start_date=start_date,
                end_date=end_date,
                defaults={
                    "completed_tasks_count": task_group['completed_tasks_count'],
                }
            )

        self.stdout.write(self.style.SUCCESS(
            "Weekly report generated successfully."
        ))
