from django.shortcuts import render

# Create your views here.
import qrcode
import jwt
from datetime import datetime, timedelta
from django.core.cache import cache
from django.http import HttpResponse
from io import BytesIO
from rest_framework.views import APIView
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from random import randint
from rest_framework.response import Response
from django.core.cache import cache
import jwt

class generate_attendance_qr(APIView):
    permission_classes = [IsAuthenticated]        
    authentication_classes = [JWTAuthentication]
    def post(self,request):
        data=request.data
        validated_data=JWTAuthentication().authenticate(request)
        user=validated_data[0]
        try:
            user=Faculty.objects.using('default').get(email=user.email)
            print(user._state.db)
            room=class_room.objects.get(room_no=data['room no'])
            sec=section.objects.get(id=data['section'])
            course=courses.objects.get(course_id=data['course'])
            print(room._state.db,sec,course)
            slot=class_slot()
            slot.save()
            slot.faculty.add(user)
            slot.room_no.add(room)
            slot.section.add(sec)
            slot.course.add(course)
            slot.save(using='default')
            token=f"{slot.token}"
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(token)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return HttpResponse(buffer.getvalue(), content_type="image/png")
        except:
            return HttpResponse("Error generating QR")

class validate_attendance_qr(APIView):
    def post(self,request):
        token = request.data.get("token")
        # token=token.split("-")[0]
        print(token)
        validated_data=JWTAuthentication().authenticate(request)
        user=validated_data[0]
        user=Student.objects.get(email=user.email)
        try:
            decoded = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
            slot=class_slot.objects.get(id=decoded.get("slot"))
            # cached_data = cache.get(token)

            # if not cached_data:
            #     return Response({"error": "Invalid or expired QR code"}, status=400)

            # # Save attendance to database
            # class_id = cached_data["class_id"]
            # timestamp = cached_data["timestamp"]
            att=attendance()
            att.save()
            att.slot.add(slot)
            att.student.add(user)
            att.save()
            # Attendance.objects.create(class_id=class_id, student_id=student_id, timestamp=timestamp)

            return Response({"message": "Attendance recorded successfully"}, status=200)

        except jwt.ExpiredSignatureError:
            return Response({"error": "QR code expired"}, status=400)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid QR code"}, status=400)
