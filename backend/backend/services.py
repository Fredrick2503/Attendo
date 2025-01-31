from qrcode import QRCode
from io import BytesIO
import uuid
import jwt
from django.conf import settings
from django.core.cache import cache
from datetime import datetime,timezone,timedelta
import random 
import string

class Qrcode:
    def createQR(self,payload):
        qr=QRCode(version=1,box_size=10,border=5)
        qr.add_data(payload)
        qr.make(fit=True)
        img=qr.make_image(fill_color="black",bacl_color="white")
        buffer=BytesIO()
        img.save(buffer,format="PNG")
        buffer.seek(0)
        print(buffer)
        return buffer.getvalue()
    


class uniqueid:
    def generateid():
        id=uuid.uuid4()
        id=str(id)
        return id.replace("-","")


class tokens:
    def generate(self,payload={},timeout=datetime.now(timezone.utc)+timedelta(minutes=1)):
        payload["exp"]=timeout
        self= jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
        now=datetime.now(timezone.utc).timestamp()
        cache.set(self,payload,timeout=(timeout.timestamp()-now))
        return self 
    
    def decode(self,token):
        try:
            self=jwt.decode(token,settings.SECRET_KEY,algorithms="HS256")
            payload=cache.get(token)
            if not payload:
                raise {"error":"Invalid QR CODE"}
            if self==payload:
                return self
                
        except jwt.ExpiredSignatureError as e:
            raise {"error":e}
        except jwt.InvalidTokenError as e:
            raise {"error":e}


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
