from django.urls import path
from .consumers import *

ws_urlpattern=[
    path("ws/client/<c_id>/",QRAttendance.as_asgi())
]