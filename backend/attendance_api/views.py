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
from backend.services import Qrcode,cache,tokens


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
from rest_framework.generics import ListAPIView
from io import BytesIO
from .serializer import studentlistserializer
import asyncio  # Required for running async Django ORM queries
from django.shortcuts import get_object_or_404

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
            course = async_to_sync(self.get_course)(data['course'])
            clientdev = async_to_sync(self.get_client)(data['client_id'])

            # Create class slot and save
            slot = class_slot()
            slot.save()
            slot.faculty.add(user)
            slot.room_no.add(room)
            slot.section.add(sec)
            slot.course.add(course)
            slot.client.add(clientdev)
            slot.save()
            print(str(slot.id))
            # sleep(20)

            # Generate QR Code
            for i in range(3):
                # token = f"{slot.token}{random.randint(1111,9999)}"
                token = slot.token
                qr_generator = Qrcode()
                qr_base64,qr_image = qr_generator.createQR(payload=token)

                # Convert QR image to base64 for WebSocket transmission
                # buffer = BytesIO(qr_image)
                # qr_base64 = base64.b4encode(qr_image.getvalue()).decode("utf-8")
                
                # Send QR Code over WebSocket (sync_to_async is needed for WebSockets)
                channel_layer = get_channel_layer()
                cli=cache.get(data["client_id"])
                if(cli):
                    cli=cli.get("channel_name")
                    # print(qr_image)
                    async_to_sync(channel_layer.send)(
                        str(cli),  # Group name must be a string
                        {
                            "type": "custom_message",
                            "value": {"data":qr_base64}  # Sending as a base64 string
                        }
                    )
                    sleep(1)
                else:
                    return JsonResponse({"error": f"No client connected"}, status=500)
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
    async def get_client(self, client_id):
        return await sync_to_async(client.objects.get)(id=client_id)


        # except Exception as e:
        #      return JsonResponse({"msg":f"Error generating QR {e}"})

class validate_attendance_qr(APIView):
    # permission_classes = [IsAuthenticated]        
    # authentication_classes = [JWTAuthentication]
    def post(self,request):
        # token = str(request.data.get("token"))
        # token=token.split("-")[0]
        # token=token[:-4]
        token=tokens()
        payload=token.decode(str(request.data.get("token")))
        print(payload)
        validated_data=JWTAuthentication().authenticate(request)
        user=validated_data[0]
        user=Student.objects.get(email=user.email)
        # try:
            # decoded = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
        try:        
            slot=class_slot.objects.get(id=payload.get("slot"))
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
            # att=attendance()
            # att.save()
            # att.slot.add(slot)
            # att.student.add(user)
            # att.save()
            # slot=f'{"".join(slot.id for slot in att.slot.all())}'.strip()
            student=Studentserializer(user).data
            cliendid=str(slot.get_clientid())
            print(cache.get(cliendid))
            host_channel=cache.get(cliendid).get("host_channel_name")
            channel_layer=get_channel_layer()
            async_to_sync(channel_layer.send)(
                host_channel,{
                    'type':"sendmsg",
                    'value': str(student)
                }
            )
            # Attendance.objects.create(class_id=class_id, student_id=student_id, timestamp=timestamp)

            return Response({"message": "Attendance recorded successfully"}, status=200)
        else:
            return Response({"message": "Attendance already recorded"}, status=200)

        # except Exception as e :
        #     return Response({"error": f"QR code expired{e}"}, status=400)
        # except :
        #     return Response({"error": "Invalid QR code"}, status=400)

class sectionlist(ListAPIView):
    serializer_class = studentlistserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs.get("section_id")  # Get 'section_id' from URL
        section_instance = get_object_or_404(section, id=section_id)  # Ensure section exists
        return student_list.objects.filter(section=section_instance)  # Filter by section

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        res={"students":[ i[0] for i in serializer.data]}
        return Response(res)
