from rest_framework import serializers
from .models import student_list
from auth_api.serializer import Studentserializer
class studentlistserializer(serializers.ModelSerializer):
    student=Studentserializer(many=True)
    class Meta:
        model=student_list
        fields=["student"]
    def to_representation(self, instance):
        students = instance.student.all()
        return [
            {
                "enrollment_id": student.enrollment_id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "semester": student.semester,
                "email": student.email,
                "phone_no": student.phone_no,
                "address": student.address,
                "department": list(student.department.values_list("dept_name", flat=True))  # Assuming department is a ManyToManyField
            }
            for student in students
        ]