from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
import json
import base64
import io
from .models import client
# from django.core.cache import cache
from backend.services import statemanager,cache
import asyncio 
class QRAttendance(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['c_id']  # Extract class ID from URL
        # self.user = self.scope['user']
        self.channel_name=self.channel_name
        # Add this WebSocket to the channel group
        # await self.channel_layer.group_add(self.id, self.channel_name)

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



class HostConnect(AsyncWebsocketConsumer):
    async def connect(self):
        self.clientid = self.scope['url_route']['kwargs']['c_id']
        self.client_channel_name=cache.get(self.clientid).get("channel_name")
        self.channel_name=self.channel_name
        client_exists = await sync_to_async(client.objects.filter(id=self.clientid).exists)()
        client_state=statemanager(self.clientid,channel_name=self.client_channel_name)
        print(client_state.getstate())
        if client_exists & (not client_state.isactive()) &(not client_state.isoffline()):

            client_state.makeactive(host_channel_name=self.channel_name)
            print(client_state.getstate())
            await self.channel_layer.group_add(self.clientid, self.channel_name)  # Correct order
            await self.accept()
            # await self.send(text_data=json.dumps({
            #     "data": {
            #         "client_id": self.clientid,
            #         "channel_name": self.channel_name
            #     }
            # }))
            await self.channel_layer.send(
                self.client_channel_name,{
                    "type":"custom_message",
                    "value":{"connections": {
                    "client_id": self.clientid,
                    "host_channel_name": self.channel_name
                }}
                }
            )
        else:
            await self.close()

    async def sendmsg(self,event):
        data=event.get('value')
        print(data)
        await self.send(text_data=json.dumps({"data": data}))

    
    async def disconnect(self,code):
        client_state=statemanager(self.clientid)
        if(not client_state.isoffline()):
            client_state.makeinactive()
        print(client_state.getstate())
        await self.send(text_data=json.dumps({"message":"disconnected"}))

    
class ClientConnect(AsyncWebsocketConsumer):
    async def connect(self):
        self.clientid = self.scope['url_route']['kwargs']['c_id']
        self.channel_name=self.channel_name
        # Check if client exists using async ORM
        client_exists = await sync_to_async(client.objects.filter(id=self.clientid).exists)()
        client_state=statemanager(self.clientid, self.channel_name)
        print(client_state.getstate())
        if client_exists:
            if(client_state.isoffline()):
                client_state.makeinactive()
                print(client_state.getstate())
                self.expiry_time = 3600  
                self.task=asyncio.create_task(self.expire_connection())
                # await self.channel_layer.group_add(self.clientid, self.channel_name)  # Correct order
                await self.accept()
            else:
                await self.close()
            # await self.send(text_data=json.dumps({
            #     "data": {
            #         "client_id": self.clientid,
            #         "channel_name": self.channel_name
            #     }
            # }))
            
        else:
            await self.close()


        # Start background task to disconnect after expiry
    async def custom_message(self, event):
        """Handles direct messages sent to this specific channel."""
        data = event.get("value")
        await self.send(text_data=json.dumps({"data": data}))

    async def expire_connection(self):
        await asyncio.sleep(self.expiry_time)
        await self.close()

    async def broadcast(self,event):
        data=event.get('value')
        # print(data)
        await self.send(text_data=json.dumps(data))

    
    async def disconnect(self,code):
        client_state=statemanager(self.clientid,channel_name=self.channel_name)
        print(code)
        if(code!=1006 and not client_state.isoffline()):
            self.task.cancel()
            client_state.makeoffline()
        await self.send(text_data=json.dumps({"message":"disconnected"}))   