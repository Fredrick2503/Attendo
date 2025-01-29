from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import random

class clientConnect(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

    def connect(self):
        self.id = self.scope['url_route']['kwargs']['c_id']  # Extract ID from the URL route
        self.user=self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            self.id, self.channel_name
        )
        print(self.user)
        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.id,{
                'type':"renderQR",
                'value':self.user.email
            }
        )
        self.send(text_data=json.dumps({"data": [self.user.email]}))

    # def connect(self):
    #     self.id=str(random.randint(111,999))
    #     self.group=(self.scope['url_route']['kwargs']['c_id'])
    #     async_to_sync(self.channel_layer.group_add)(
    #         self.id,self.group 
    #     )
    #     # print(self,vars(self))
    #     self.accept()
    #     self.send(text_data=json.dumps({"data":[self.id]}))



    def receive(self, text_data=None, bytes_data=None):
        # self.send(text_data=text_data)
        print(self.id,self.groups)
        async_to_sync(self.channel_layer.group_send)(
            self.id,{
                'type':"renderQR",
                'value':text_data
            }
        )
        return super().receive(text_data, bytes_data)
    
    def renderQR(self,event):
        self.send(text_data=(event.get('value')))
        print(event)



class cilent_connet(WebsocketConsumer):
    def connect(self):
        self.clientid = self.scope['url_route']['kwargs']['c_id']
        return super().connect()