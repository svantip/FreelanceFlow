from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import Project, Task


def send_websocket_notification(user_id, event_type, message):
    """
    Utility function to send WebSocket notifications to a specific user using an event type and a message.
    """
    channel_layer = get_channel_layer()
    event = {
        "type": event_type,  # Custom WebSocket message type
        "text": message,  # Message text sent to the consumer
    }
    async_to_sync(channel_layer.group_send)(f"user_{user_id}", event)


# Signal to notify only the project owner when a project is created or updated
@receiver(post_save, sender=Project)
def notify_project_owner(sender, instance, created, **kwargs):
    if created:
        # Notify the project owner about the creation of a project
        send_websocket_notification(
            user_id=instance.owner.id,
            event_type="project_created",  # Event type
            message=f"You created a new project: '{instance.project_name}'.",
        )
    else:
        # Notify the project owner about updates to their project
        send_websocket_notification(
            user_id=instance.owner.id,
            event_type="project_updated",  # Event type
            message=f"Your project '{instance.project_name}' has been updated.",
        )


# Signal to notify only the project owner when a task is created or updated
@receiver(post_save, sender=Task)
def notify_task_owner(sender, instance, created, **kwargs):
    project = instance.project
    if created:
        # Notify the project owner about a new task
        send_websocket_notification(
            user_id=project.owner.id,
            event_type="task_created",  # Event type
            message=f"A new task '{instance.task_name}' was created in your project '{project.project_name}'.",
        )
    else:
        # Notify the project owner about updates to a task
        send_websocket_notification(
            user_id=project.owner.id,
            event_type="task_updated",  # Event type
            message=f"The task '{instance.task_name}' in your project '{project.project_name}' has been updated.",
        )
