from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64
import io
class QRAttendance(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['c_id']  # Extract class ID from URL
        # self.user = self.scope['user']

        # Add this WebSocket to the channel group
        await self.channel_layer.group_add(self.id, self.channel_name)

        # print(self.user)
        await self.accept()

    async def send_qr_image(self, event):
        """Reads and sends an image as Base64 over WebSockets."""
        # image_buffer=io.BytesIO(event.get("path"))
        print(event)
        # base64_image = base64.b64encode(image_buffer.getvalue()).decode("utf-8")
        text_data=json.dumps({"image": event.get("path")})
        await self.send(text_data=text_data)   

        # Send initial data to the group
        await self.channel_layer.group_send(
            self.id, {
                'type': "renderQR",
                'value': text_data
            }
        )

    async def receive(self, text_data=None, bytes_data=None):
        print(self.id, self.groups)

        # Send received message to the group
        await self.channel_layer.group_send(
            self.id, {
                'type': "renderQR",
                'value': text_data
            }
        )

    async def renderQR(self, event):
        # Send event data to WebSocket client
        await self.send(text_data=json.dumps({"value": event.get('value')}))
        print(event)

    async def disconnect(self, close_code):
        # Remove WebSocket from the channel group
        await self.channel_layer.group_discard(self.id, self.channel_name)



class cilent_connet(AsyncWebsocketConsumer):
    def connect(self):
        self.clientid = self.scope['url_route']['kwargs']['c_id']
        return super().connect()