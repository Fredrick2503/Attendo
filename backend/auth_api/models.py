from django.db import models
# from users.models import CustomUser
# Create your models here.
# class profile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
#     first_name=models.CharField(max_length=50,null=False,blank=False)
#     last_name=models.CharField(max_length=50,null=False,blank=False)
#     phone_no=models.CharField(max_length=15,null=False,blank=False)
#     address=models.CharField(max_length=200,null=False,blank=False)
#     # profile_pic=models.ImageField()
#     def __str__(self):
#         return f'{self.first_name} {self.last_name} ({self.user})'

class department(models.Model):
    dept_id=models.CharField(max_length=2,primary_key=True)
    dept_name=models.CharField(max_length=50)
    def __str__(self) -> str:
        return f'{self.dept_name} ({self.dept_id})'
    def get_dept(self):
        return f'{self.dept_name} ({self.dept_id})'

# class courses(models.Model):
#     course_id=models.CharField(max_length=7,null=False,unique=True,primary_key=True)
#     course_name=models.CharField(max_length=30,null=False,unique=True)
#     dept=models.OneToOneField(department,on_delete=models.CASCADE,related_name="course_in_department")
#     credit=models.IntegerField()
#     def __str__(self) -> str:
#         return f'{self.course_name} ({self.course_id})'

# class FacultyProfile(models.Model):
#     profile=models.OneToOneField(profile,on_delete=models.CASCADE,related_name="faculty_profile")
#     facuty_id=models.CharField(max_length=50,unique=True,primary_key=True,null=False)
#     dept=models.OneToOneField(department,on_delete=models.SET_NULL,related_name="faculty_department",null=True)
#     courses = models.ManyToManyField('courses')
#     def get_id(self):
#         return self.enrollment_id
#     def __str__(self):
#         return f'{self.profile.first_name} {self.profile.last_name}({self.facuty_id})'


# class StudentProfile(models.Model):
#     profile = models.OneToOneField(profile, on_delete=models.CASCADE, related_name='student_profile')
#     enrollment_id = models.CharField(max_length=50,unique=True,primary_key=True,null=False)
#     dept=models.OneToOneField(department,on_delete=models.SET_NULL,related_name="student_department",null=True)

#     def get_id(self):
#         return self.enrollment_id

#     def __str__(self):
#         return f'{self.profile.first_name} {self.profile.last_name} ({self.enrollment_id})'