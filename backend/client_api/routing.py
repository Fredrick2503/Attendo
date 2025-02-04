from django.urls import path
from .consumers import *

ws_urlpattern=[
    path("ws/client/<c_id>/",ClientConnect.as_asgi()),
    path("ws/hsclient/<c_id>/",HostConnect.as_asgi()),
    path("ws/hsclient/<c_id>/<slot_id>",HostConnect.as_asgi()),

]