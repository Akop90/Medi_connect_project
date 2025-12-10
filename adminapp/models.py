from django.db import models

# Create your models here.
class StaffRequest(models.Model):
    staff_name = models.CharField(max_length=100)
    staff_email = models.EmailField(max_length=100)
    staff_password = models.CharField(max_length=100)
    staff_phone = models.CharField(max_length=20)
    staff_address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_name
    

class StaffRegister(models.Model):
    staff_name = models.CharField(max_length=100)
    staff_email = models.EmailField()
    staff_password = models.CharField(max_length=100)
    staff_phone = models.CharField(max_length=20)
    staff_address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_name


class DoctorRequest(models.Model):
    doctor_id = models.CharField(max_length=20)
    doctor_name = models.CharField(max_length=100)
    doctors_speciality = models.CharField(max_length=80)
    doctor_email = models.EmailField()
    doctor_phone = models.CharField(max_length=20)
    doctor_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor_name} - {self.doctors_speciality}"
    


class DoctorRegister(models.Model):
    doctor_id = models.CharField(max_length=20, primary_key=True)
    doctor_name = models.CharField(max_length=100)
    doctors_speciality = models.CharField(max_length=80)
    doctor_email = models.EmailField()
    doctor_phone = models.CharField(max_length=20)
    doctor_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor_name} - {self.doctors_speciality}"
    

# models.py
class Notification(models.Model):
    message = models.TextField()
    send_to = models.CharField(max_length=10, choices=(('doctor', 'Doctor'), ('staff', 'Staff')))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.send_to}: {self.message[:30]}"


class Bill(models.Model):
    appointment = models.OneToOneField('mainapp.Appointment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Bill for {self.appointment.name} - {self.amount}"


def some_function():
    from adminapp.models import DoctorRegister
    # use DoctorRegister here





















