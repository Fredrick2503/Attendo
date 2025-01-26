
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
# from .models import StudentProfile,profile,FacultyProfile,department,courses
from users.models import *
from .serializer import loginserializer,Studentserializer,Facultyserializer
from datetime import timedelta
# # Create your views here.


class logout(APIView):
    def post(self,request):
        return Response({  
            "data": {},
            "message": "User logged out",
            "statusCode": 200,
            "success": True})

# #Login endpoint to fetch accestoken and userdata on login
class login(APIView):
    def post(self, request):
        data = loginserializer(data=request.data)
        if data.is_valid():
            user = data.validated_data['user']
            profile=data.validated_data['profile']
            # print(Student.objects.get(id=user.id))
            #Studentserializer return user profile and student data from database 
            # user_profile=Studentserializer(StudentProfile.objects.get(profile=profile.objects.get(user=user))).data
            #RefreshToken returns a token for user
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "Authentication successful.",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "token_type": "Bearer",
                "data": {
                    "expires_in": timedelta(hours=1),
                    "user": profile,
            }})
        else:
            return Response({
                "success": False,
                "message": "Invalid credentials. Please check your username and password.",
                "data": None,
                "errors": data.errors
            }
            )
        


class profileview(APIView):
    permission_classes = [IsAuthenticated]        
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        validated_data=JWTAuthentication().authenticate(request)
        user=validated_data[0]
        try:
            if user.is_student():
                user=Student.objects.get(email=user.email)
                profile_data = Studentserializer(user).data
            if user.is_faculty():
                user=Faculty.objects.get(email=user.email)
                profile_data = Facultyserializer(user).data
        except:
            ValueError
        if not profile_data:
            pass
        return Response({
    "success": True,
    "message": "User details fetched successfully.",
    "data": profile_data
})