from django.contrib.auth.models import User
from django.db import models
from adminapp.models import DoctorRegister

# Create your models here.

class AdminLogin(models.Model):
    userid=models.CharField(max_length=50)
    password=models.CharField(max_length=50)


class Complaints(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    complaint = models.TextField()
    registered_date=models.DateField()


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    symptoms = models.TextField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    doctor_speciality = models.CharField(max_length=80)
    doctor = models.ForeignKey(DoctorRegister, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} → {self.doctor.doctor_name}"


class AccountantRegister(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    registered_at = models.DateTimeField(auto_now_add=True)

class AccountantRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    is_discharged = models.BooleanField(default=False)

    def __str__(self):
        return self.name












