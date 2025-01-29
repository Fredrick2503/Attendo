from django.db import models
import uuid
from attendance_api.models import class_room
# Create your models here.
class client(models.Model):
    id=models.CharField(default=("".join(str(uuid.uuid4()).split("-"))),max_length=36,unique=True,editable=True,primary_key=True)
    room_no=models.OneToOneField(class_room,on_delete=models.SET_NULL,null=True)
    is_active=models.BooleanField(default=False)
