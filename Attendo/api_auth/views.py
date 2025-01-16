from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from api_auth.serializer import loginserializers,MyTokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class profile(APIView):
  def get(self,request):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    return Response({
  "success": True,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "johndoe@example.com",
      "profile": {
        "first_name": "John",
        "last_name": "Doe"
      }
    }
  }
})


# class login(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self,request):
#         return Response({'msg':'hello'})
#     def post(self,request):
#         data=loginserializers(data=request.data)
#         if data.is_valid():
#             user = authenticate(username=data.validated_data['username'],password=data.validated_data['password'])
#             if user != None:
                
#                 return Response({
#   "success": True,
#   "message": "Login successful",
#   "data": {
#     "access_token": "your_access_token",
#     "refresh_token": "your_refresh_token",
#     "user": {
#       "id": 1,
#       "username": "johndoe",
#       "email": "johndoe@example.com",
#       "profile": {
#         "first_name": "John",
#         "last_name": "Doe"
#       }
#     }
#   }
# }

# )
#             return Response({
#   "success": False,
#   "message": "Invalid username or password",
#   "errors": {"Invalid credentials"
#   }
# }
# )
#         return Response({
#   "success":False,
#   "message": "Invalid username or password",
#   "errors": 
#     data.errors
# }
# )
        
