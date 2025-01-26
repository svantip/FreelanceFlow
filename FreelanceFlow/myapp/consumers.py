import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f"user_{self.scope['user'].id}"
        # Join the user to their own unique room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        # Log the received data
        text_data_json = json.loads(text_data)
        event_type = text_data_json["type"]
        message = text_data_json["text"]
        print(f"Received: {event_type} - {message}")

        # Send back the message to the WebSocket (echoing)
        await self.send(text_data=json.dumps({"event": event_type, "message": message}))

    # Handle different event types
    async def project_created(self, event):
        await self.send(
            text_data=json.dumps({"event": "project_created", "message": event["text"]})
        )

    async def project_updated(self, event):
        await self.send(
            text_data=json.dumps({"event": "project_updated", "message": event["text"]})
        )

    async def task_created(self, event):
        await self.send(
            text_data=json.dumps({"event": "task_created", "message": event["text"]})
        )

    async def task_updated(self, event):
        await self.send(
            text_data=json.dumps({"event": "task_updated", "message": event["text"]})
        )
