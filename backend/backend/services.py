from qrcode import QRCode
from io import BytesIO
import uuid
import jwt
from django.conf import settings
from django.core.cache import cache
from datetime import datetime,timezone,timedelta
import random 
import string
import base64
from jwt.exceptions import ExpiredSignatureError, DecodeError

class Qrcode:
    def createQR(self,payload):
        qr=QRCode(version=3,box_size=10,border=5)
        qr.add_data(payload)
        qr.make(fit=True)
        img=qr.make_image(fill_color="black",bacl_color="white")
        buffer=BytesIO()
        img.save(buffer,format="PNG")
        buffer.seek(0)
        Qr=base64.b64encode(buffer.getvalue()).decode("utf-8")
        # print(Qr)
        return (Qr,buffer)
    


class uniqueid:
    def generateid():
        id=uuid.uuid4()
        id=str(id)
        return id.replace("-","")


class tokens:
    def generate(self, payload={}, timeout_minutes=180):
        """Generates a JWT token and caches it with an expiry time."""
        
        now = datetime.now(timezone.utc)
        exp_time = now + timedelta(minutes=timeout_minutes)
        
        payload["iat"] = now.timestamp()  # Issued at
        payload["exp"] = exp_time.timestamp()  # Expiry time
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        
        # Store token in cache until expiration
        cache.set(token, payload, timeout=(exp_time - now).total_seconds())

        print("Generated Token:", token)
        print("Cached Payload:", cache.get(token))

        return token 

    def decode(self, token):
        """Decodes a JWT token and validates against cache."""
        try:
            print("Received Token:", token)
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Retrieve from cache for additional validation
            cached_payload = cache.get(token)
            # if not cached_payload:
            #     raise Exception("Token is invalid or expired.")

            return decoded_payload
        
        except ExpiredSignatureError:
            raise Exception("Token has expired. Please log in again.")
        except DecodeError:
            raise Exception("Invalid token. Authentication failed.")

class passwordgenrator:
    def make(size=8, chars=string.ascii_uppercase+ string.ascii_lowercase+ string.digits):
        return ''.join(random.choice(chars) for _ in range(size))



class mailer:
    def __init__(self,to=str(),body=str(),subject=str()):
        self.to=to
        self.subject=subject
        
        self.body=body
    def send(self):
        print(f"----------------------------------------------\nTo:{self.to}\nSubject:f{self.subject}\n\nBody:\nf{self.body}\n----------------------------------------------")


class statemanager:
    def __init__(self,id,channel_name,host_channel_name=None):
        self.id=id
        # self.state="offline"
        clientstate=cache.get(self.id)
        if not clientstate:   
            cache.set(self.id,{"state":"offline","channel_name":channel_name,"host_channel_name":host_channel_name},timeout=600)

    def makeactive(self,host_channel_name):
        clientstate=cache.get(self.id)
        if clientstate:
            # self.state="active"
            clientstate['state']="active"
            clientstate["host_channel_name"]=host_channel_name
            cache.set(self.id,clientstate,timeout=600)
        else:
            cache.set(self.id,{'state':"active"},timeout=(600))
    def makeinactive(self):
        clientstate=cache.get(self.id)
        if clientstate:
            # self.state="inactive"
            clientstate['state']="inactive"

            cache.set(self.id,clientstate,600)
        else:
            cache.set(self.id,{'state':"inactive"},timeout=(600))
    
    def makeoffline(self):
        clientstate=cache.get(self.id)
        if clientstate:
            # self.state="offline"
            clientstate['state']="offline"
            cache.set(self.id,clientstate,600)
        else:
            cache.set(self.id,{'state':"offline"},timeout=(600))

    def isactive(self):
        clientstate=cache.get(self.id)
        if clientstate:
            return clientstate["state"]=="active"
        return False
    def isinactive(self):
        clientstate=cache.get(self.id)
        if clientstate:
            return clientstate["state"]=="inactive"
        return False
    def isoffline(self):
        clientstate=cache.get(self.id)
        if clientstate:
            return clientstate["state"]=="offline"
        return True
    def getstate(self):
        return cache.get(self.id).get("state")
    
        