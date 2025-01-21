import os
import sys
from celery import Celery

# Ensure the project directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreelanceFlow.settings')

app = Celery('FreelanceFlow')

# Load settings from Django settings, using the 'CELERY' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all installed apps
app.autodiscover_tasks()
