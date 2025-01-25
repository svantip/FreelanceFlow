from django.core.management.base import BaseCommand
from myapp.models import Project, WeeklyReport
from django.utils.timezone import now
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate weekly reports for all ongoing projects'

    def handle(self, *args, **kwargs):
        # Define the reporting time range
        end_date = now()
        start_date = end_date - timedelta(days=7)

        # Delete existing reports for this time range
        WeeklyReport.objects.filter(start_date=start_date, end_date=end_date).delete()
        logger.info(f"Cleared existing reports for the period {start_date} to {end_date}.")

        # Get all ongoing projects
        projects = Project.objects.filter(project_status='ongoing')
        reports = []

        for project in projects:
            # Calculate task stats for the reporting period
            completed_tasks_count = project.tasks.filter(
                task_status='completed',
                task_updated__range=[start_date, end_date]
            ).count()

            total_tasks_count = project.tasks.filter(
                task_updated__range=[start_date, end_date]
            ).count()

            if total_tasks_count == 0:
                logger.info(f"Skipping project '{project.project_name}' with no tasks updated in the last week.")
                continue

            completion_percentage = (completed_tasks_count / total_tasks_count * 100)

            # Create a new report for the project
            report = WeeklyReport(
                project=project,
                completed_tasks_count=completed_tasks_count,
                start_date=start_date,
                end_date=end_date,
                completion_percentage=completion_percentage
            )
            reports.append(report)

        # Save all reports in bulk
        if reports:
            WeeklyReport.objects.bulk_create(reports)
            logger.info(f"Generated {len(reports)} new reports.")

        self.stdout.write(self.style.SUCCESS('Weekly reports generated successfully.'))
