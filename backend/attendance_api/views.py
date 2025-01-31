from django.shortcuts import render
from time import sleep
# Create your views here.
from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from random import randint
from rest_framework.response import Response
from auth_api.serializer import Studentserializer
from .models import student_list
from backend.services import Qrcode


# class generate_attendance_qr(APIView):
#     permission_classes = [IsAuthenticated]        
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]        
#     authentication_classes = [JWTAuthentication]
#     def post(self,request):
        
#         data=request.data
#         validated_data=JWTAuthentication().authenticate(request)
#         user=validated_data[0]
        
#         user=Faculty.objects.using('default').get(email=user.email)
#         # print(user._state.db)
#         room=class_room.objects.get(room_no=data['room no'])
#         sec=section.objects.get(id=data['section'])
#         course=courses.objects.get(course_id=data['course'])
#         # print(room._state.db,sec,course)
#         slot=class_slot()
#         slot.save()
#         slot.faculty.add(user)
#         slot.room_no.add(room)
#         slot.section.add(sec)
#         slot.course.add(course)
#         slot.save(using='default')
#         token=f"{slot.token}"
#         QR=Qrcode()
#         QR=QR.createQR(payload=token)
#         channel_layer=get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             slot,{
#                 'type':"renderQR",
#                 'path': QR
#             }
#         )
#         return HttpResponse(QR, content_type="image/png")


from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async, async_to_sync
from backend.services import Qrcode
from channels.layers import get_channel_layer
import base64
from io import BytesIO
import asyncio  # Required for running async Django ORM queries

class generate_attendance_qr(APIView):
    permission_classes = [IsAuthenticated]        
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            data = request.data

            # Authenticate user (Sync call to avoid async context issues)
            validated_data = JWTAuthentication().authenticate(request)
            if validated_data is None:
                return JsonResponse({"error": "Authentication failed"}, status=401)

            user = validated_data[0]
            
            # Perform database queries inside a sync_to_async block
            user = async_to_sync(self.get_faculty)(user.email)
            room = async_to_sync(self.get_classroom)(data['room no'])
            sec = async_to_sync(self.get_section)(data['section'])
            course = async_to_sync(self.get_course)(data['course'])

            # Create class slot and save
            slot = class_slot()
            slot.save()
            slot.faculty.add(user)
            slot.room_no.add(room)
            slot.section.add(sec)
            slot.course.add(course)
            slot.save()

            # Generate QR Code
            token = f"{slot.token}"
            qr_generator = Qrcode()
            qr_image = qr_generator.createQR(payload=token)

            # Convert QR image to base64 for WebSocket transmission
            buffer = BytesIO(qr_image)
            qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Send QR Code over WebSocket (sync_to_async is needed for WebSockets)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                str(123),  # Group name must be a string
                {
                    "type": "send_qr_image",
                    "path": qr_base64  # Sending as a base64 string
                }
            )
            print(str(slot.id))
            # sleep(20)
            return HttpResponse(qr_image, content_type="image/png")

        except Exception as e:
            return JsonResponse({"error": f"Error generating QR: {str(e)}"}, status=500)

    # Django ORM queries wrapped in sync_to_async
    async def get_faculty(self, email):
        return await sync_to_async(Faculty.objects.get)(email=email)

    async def get_classroom(self, room_no):
        return await sync_to_async(class_room.objects.get)(room_no=room_no)

    async def get_section(self, section_id):
        return await sync_to_async(section.objects.get)(id=section_id)

    async def get_course(self, course_id):
        return await sync_to_async(courses.objects.get)(course_id=course_id)


        # except Exception as e:
        #      return JsonResponse({"msg":f"Error generating QR {e}"})

class validate_attendance_qr(APIView):
    permission_classes = [IsAuthenticated]        
    authentication_classes = [JWTAuthentication]
    def post(self,request):
        token = request.data.get("token")
        # token=token.split("-")[0]
        print(token)
        validated_data=JWTAuthentication().authenticate(request)
        user=validated_data[0]
        user=Student.objects.get(email=user.email)
        try:
            # decoded = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
            # slot=class_slot.objects.get(id=decoded.get("slot"))
            try:        
                c_list=student_list.objects.get(student=user)
            except:
                return JsonResponse({
                    'msg':'Invalid Qr'
                })
            # cached_data = cache.get(token)
            # print(cached_data)
            # if not cached_data:
                # return Response({"error": "Invalid or expired QR code"}, status=400)

            # # Save attendance to database
            # class_id = cached_data["class_id"]
            # timestamp = cached_data["timestamp"]
            if not (attendance.objects.filter(slot=slot,student=user).exists()):
                att=attendance()
                att.save()
                att.slot.add(slot)
                att.student.add(user)
                att.save()
                slot=f'{"".join(slot.id for slot in att.slot.all())}'.strip()
                student=Studentserializer(user).data
                print(slot)
                channel_layer=get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    slot,{
                        'type':"renderQR",
                        'value': str(student)
                    }
                )
                # Attendance.objects.create(class_id=class_id, student_id=student_id, timestamp=timestamp)

                return Response({"message": "Attendance recorded successfully"}, status=200)
            else:
                return Response({"message": "Attendance already recorded"}, status=200)

        except :
            return Response({"error": "QR code expired"}, status=400)
        # except :
        #     return Response({"error": "Invalid QR code"}, status=400)
