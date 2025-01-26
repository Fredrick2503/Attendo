from dataclasses import fields
from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import CustomUser,Student,Faculty
# from .models import profile,StudentProfile
# from rest_framework_simplejwt.tokens import RefreshToken




# class profileserializer(serializers.ModelSerializer):
#     class Meta:
#         model=profile
#         fields=('first_name','last_name')



class Studentserializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['enrollment_id','first_name','last_name','semester','email','phone_no','address','department']
class Facultyserializer(serializers.ModelSerializer):
    class Meta:
        model=Faculty
        fields=['faculty_id','first_name','last_name','email','phone_no','address','department']
        
class loginserializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        errs = {}
        if not email:
            errs["email"] = "Email address is required to log in. "
        if not password:
            errs["password"] = "Password is required to log in."
        user = authenticate(email=email, password=password)
        if not user:
            errs["non_field_errors"] = "Invalid credentials"

        if errs:
            raise serializers.ValidationError(errs)
        # Attach user object to validated data for use in the view
        if user.is_student():
            attrs["user"]=Student.objects.get(email=user.email)
            attrs["profile"] = Studentserializer(attrs["user"]).data
        if user.is_faculty():
            attrs["user"] = Faculty.objects.get(email=user.email)
            attrs["profile"] = Facultyserializer(attrs["user"]).data
        
        return attrs

