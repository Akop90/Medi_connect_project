from adminapp import views
from django.contrib import admin
from django.urls import path
from . import views

app_name='adminapp'

urlpatterns = [
   path('',views.adminhome,name='adminhome'),
   path('adminhome',views.adminhome,name='adminhome'),
   path('adminlogiut',views.adminlogout,name='adminlogout'),
   path('addstaff/',views.addstaff,name='addstaff'),
   path('viewstaffrequest/', views.viewstaffrequest, name='viewstaffrequest'),
   path('acceptstaffrequest/<int:id>/', views.acceptstaffrequest, name='acceptstaffrequest'),
   path('deletestaffrequest/<int:id>/', views.deletestaffrequest, name='deletestaffrequest'),
   path('viewdoctorrequest/',views.viewdoctorrequest,name='viewdoctorrequest'),
   path('adddoctor/',views.adddoctor,name='adddoctor'),
   path('acceptdoctorrequest/<int:id>/', views.acceptdoctorrequest, name='acceptdoctorrequest'),
   path('deletedoctorrequest/<int:id>/', views.deletedoctorrequest, name='deletedoctorrequest'),
   path('viewdoctor/',views.viewdoctor,name='viewdoctor'),
   path('viewstaff/',views.viewstaff,name='viewstaff'),
   path('viewcomplaints/', views.viewcomplaints, name='viewcomplaints'),
   path('deletecomplaint/<int:id>/', views.deletecomplaint, name='deletecomplaint'),
   path('addnotification/',views.addnotification,name='addnotification'),
   path('viewnotifi/',views.viewnotifi,name='viewnotifi'),
   path('deletenotification/<int:id>/', views.deletenotification, name='deletenotification'),
   path('dkp/<str:doctor_id>/', views.dkp, name='dkp'),
   path('deletestaff/<int:id>/', views.deletestaff, name='deletestaff'),
   path('billing/', views.billing, name='billing'),
   path('billing/create/<int:appointment_id>/', views.create_bill, name='create_bill'),
   path('billing/mark_paid/<int:bill_id>/', views.mark_bill_paid, name='mark_bill_paid'),
   path('accountant/requests/', views.view_accountant_requests, name='view_accountant_requests'),
   path('accountant/approve/<int:req_id>/', views.approve_accountant, name='approve_accountant'),
   path('accountant/decline/<int:req_id>/', views.decline_accountant, name='decline_accountant'),
   path('accountant/list/', views.view_accountants, name='view_accountants'),
   path('accountant/delete/<int:acc_id>/', views.delete_accountant, name='delete_accountant'),
   # Receptionist admin routes removed
]