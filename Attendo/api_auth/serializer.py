from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        token= super().validate(attrs)
        refresh = self.get_token(self.user)
        data={}
        data["success"]=True
        data["message"]= "Login successful",
        data["data"]= {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "username":self.user.username
            }
        }
        return data

class loginserializers(serializers.Serializer):
    username=serializers.CharField(max_length=16)
    password=serializers.CharField(max_length=100) 