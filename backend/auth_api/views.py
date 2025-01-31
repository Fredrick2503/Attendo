from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import *
from rest_framework import status
from .serializer import loginserializer, Studentserializer, Facultyserializer, ChangePasswordSerializer
from datetime import timedelta


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({  
            "data": {},
            "message": "User logged out successfully.",
            "statusCode": status.HTTP_200_OK,
            "success": True
        }, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        data = loginserializer(data=request.data)
        if data.is_valid():
            user = data.validated_data['user']
            profile = data.validated_data['profile']

            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "success": True,
                "message": "Authentication successful.",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "token_type": "Bearer",
                "data": {
                    "expires_in": timedelta(hours=1).total_seconds(),  # Convert timedelta to seconds
                    "user": profile,
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Invalid credentials. Please check your username and password.",
            "data": None,
            "errors": data.errors
        }, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                "success": True,
                "message": "Password updated successfully."
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "message": "Password update failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]        
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        validated_data = JWTAuthentication().authenticate(request)
        user = validated_data[0]

        profile_data = None
        if user.is_student():
            user = Student.objects.get(email=user.email)
            profile_data = Studentserializer(user).data
        elif user.is_faculty():
            user = Faculty.objects.get(email=user.email)
            profile_data = Facultyserializer(user).data

        if profile_data is None:
            return Response({
                "success": False,
                "message": "User profile not found."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "success": True,
            "message": "User details fetched successfully.",
            "data": profile_data
        }, status=status.HTTP_200_OK)
