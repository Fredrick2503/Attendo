
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
# from .models import StudentProfile,profile,FacultyProfile,department,courses
from users.models import *
from .serializer import loginserializer
from datetime import timedelta
# # Create your views here.

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
        


# class profileview(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self,request,enrollment_id):
#         # authentication_classes = [JWTAuthentication]
#         profile_data=Studentserializer(StudentProfile.objects.get(enrollment_id=enrollment_id)).data
#         print(profile_data)
#         if not profile_data:
#             pass
#         return Response({
#     "success": True,
#     "message": "User details fetched successfully.",
#     "data": {
#         "first_name":profile_data['profile']['first_name'],
#         "last_name": profile_data['profile']['last_name'],
#         "enrollment_id":profile_data["enrollment_id"],
#         "department":(department.objects.get(dept_id=profile_data['dept'])).get_dept(),
#     }
# })