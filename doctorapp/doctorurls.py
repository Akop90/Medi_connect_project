from doctorapp import views
from django.urls import path
app_name='doctorapp'

urlpatterns = [
   path('',views.doctorhome,name='doctorhome'),
   path('doctorhome',views.doctorhome,name='doctorhome'),
   path('vpa/',views.vpa,name='vpa'),
   path('markaproove/<int:id>/', views.markaproove, name='markaproove'),
   path('deleteappointment/<int:id>/', views.deleteappointment, name='deleteappointment'),
   path('reschedule/<int:app_id>/', views.reschedule_appointment, name='reschedule_appointment'),
   path('doctorlogout/',views.doctorlogout,name='doctorlogout'),
   path('vnoti/',views.vnoti,name='vnoti'),
   path('profile/', views.profile, name='profile'),
   path('profile/edit/', views.edit_profile, name='edit_profile'),
]