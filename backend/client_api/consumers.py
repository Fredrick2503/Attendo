from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class clientConnect(WebsocketConsumer):
    def connect(self):
        # self.room_name="hello"
        # self.room_group_name="lost"
        id=(self.scope['url_route']['kwargs']['c_id'])
        async_to_sync(self.channel_layer.group_add)(
            "client" , id
        )
        print(self,vars(self))
        self.accept()
        self.send(text_data=json.dumps({"data":["helloa"]}))


    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=text_data)
        return super().receive(text_data, bytes_data)