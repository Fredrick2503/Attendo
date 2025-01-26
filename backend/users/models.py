from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from auth_api.models import department
import uuid

# Define roles
class Roles(models.TextChoices): 
    ADMIN = "ADMIN", "admin"
    STUDENT = "STUDENT", "student"
    FACULTY = "FACULTY", "faculty"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, role, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role="ADMIN", password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.is_active = True  # Ensure the superuser is active
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)

class CustomUser(AbstractBaseUser):
    # id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(max_length=50, verbose_name="email", unique=True, primary_key=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=True)
    phone_no = models.CharField(max_length=15, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(default=False)  # Superuser status
    role = models.CharField(max_length=20, choices=Roles.choices)

    # Specify the username field and required fields
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    # Associate the custom manager
    objects = CustomUserManager()

    def get_role(self):
        return self.get_role_display()

    def get_id(self):
        return self.id

    def is_student(self):
        return self.role == Roles.STUDENT

    def is_faculty(self):
        return self.role == Roles.FACULTY

    def is_admin(self):
        return self.role == Roles.ADMIN

    def has_perm(self, perm, obj=None):
        """Grant all permissions to superusers."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Grant access to all app modules to superusers."""
        return self.is_superuser

    def __str__(self):
        return f'{self.email} ({self.get_role()})'

class StudentManager(CustomUserManager):
    def create_user(self, email, password=None, **extra_fields):
        return super().create_user(email, role=Roles.STUDENT, password=password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(role=Roles.STUDENT)

class Student(CustomUser):
    enrollment_id=models.CharField(max_length=10,unique=True)
    department=models.OneToOneField(department,on_delete=models.SET_NULL,null=True)
    semester=models.IntegerField(default=1)
    objects = StudentManager()

    def save(self, *args, **kwargs):
        self.role = Roles.STUDENT
        super().save(*args, **kwargs)

class FacultyManager(CustomUserManager):
    def create_user(self, email, password=None, **extra_fields):
        return super().create_user(email, role=Roles.FACULTY, password=password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(role=Roles.FACULTY)

class Faculty(CustomUser):
    faculty_id=models.CharField(max_length=10,unique=True)
    department=models.ForeignKey(department,on_delete=models.SET_NULL,null=True)
    objects = FacultyManager()

    def save(self, *args, **kwargs):
        self.role = Roles.FACULTY
        super().save(*args, **kwargs)
