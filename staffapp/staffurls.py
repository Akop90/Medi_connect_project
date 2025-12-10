from staffapp import views
from django.contrib import admin
from django.urls import path
app_name='staffapp'

urlpatterns = [
   path('',views.staffhome,name='staffhome'),
   path('staffhome',views.staffhome,name='staffhome'),
   path('viewnoti/',views.viewnoti,name='viewnoti'),
   path('stafflogout',views.stafflogout,name='stafflogout'),
 
]