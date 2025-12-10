from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(StaffRequest)
admin.site.register(StaffRegister)
admin.site.register(DoctorRequest)
admin.site.register(DoctorRegister)
admin.site.register(Notification)
from .models import Bill

admin.site.register(Bill)

