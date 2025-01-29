from django.db import models
import uuid
from users.models import Faculty,Student
from auth_api.models import class_room,courses,department
from datetime import datetime, timedelta
from django.core.cache import cache
import jwt
from backend.settings import SECRET_KEY
from asgiref.sync import async_to_sync
from channels.layers import *
import json
# Create your models here.

class section(models.Model):
    
    id = models.CharField(max_length=36,default=uuid.uuid4,primary_key=True,unique=True, editable=True)
    section=models.CharField(max_length=5)
    department=models.ManyToManyField(department)
    mentor=models.ManyToManyField(Faculty)
    def __str__(self):
        return f'{self.department.get()} {self.section}'
    

class class_slot(models.Model):
    id = models.CharField(default=("".join((str(uuid.uuid4()).split('-')))),max_length=36,primary_key=True,unique=True, editable=True)
    faculty=models.ManyToManyField(Faculty)
    room_no=models.ManyToManyField(class_room)
    section=models.ManyToManyField(section)
    course=models.ManyToManyField(courses)
    timestamp=models.DateTimeField(auto_now_add=True)
    token=models.CharField(max_length=250,blank=True)

    def generate_attendance_token(self):
        payload = {
            'slot':str(self.id),
            "timestamp": str(self.timestamp),
        }
        token = jwt.encode(payload,SECRET_KEY, algorithm="HS256")
        cache.set(token, {"class_id": self.id, "timestamp": payload["timestamp"]}, timeout=900)
        return token
    # def save(self,*args,**kwargs):
    #     self.token=self.generate_attendance_token()
    #     super().save(*args,**kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save before generating the token
        self.token = self.generate_attendance_token()
        cache.set(self.token, {"class_id": self.id, "timestamp": str(self.timestamp)}, timeout=900)
        # layer=get_channel_layer()
        # async_to_sync(layer.group_add)(
        #     "client" , ticket
        # )
        # async_to_sync(layer.group_send)(
        #     ticket,{
        #         'type':"renderQR",
        #         'value': json.dumps({"token":""})
        #     }
        # )
        # print(self,vars(self))
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{", ".join([room.room_no for room in self.room_no.all()])} {", ".join([sec.section for sec in self.section.all()])} ({self.timestamp})'


class attendance(models.Model):
    slot=models.ManyToManyField(class_slot)
    student=models.ManyToManyField(Student)

    # def save(self,*args,**kwargs):
    #     super().save(*args,**kwargs)
        
    #     return super().save(*args,**kwargs)


    
class student_list(models.Model):
    section=models.ManyToManyField(section)
    student=models.ManyToManyField(Student)