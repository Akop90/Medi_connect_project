from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('staffregister/', views.staffregister, name='staffregister'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('cashless_part/', views.cashless_part, name='cashless_part'),
    path('doctors/', views.doctors, name='doctors'),
    path('facilities/', views.facilities, name='facilities'),
    path('doctorregister/', views.doctorregister, name='doctorregister'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('mkap/', views.mkap, name='mkap'),
    path('accountantregister/', views.accountantregister, name='accountantregister'),
    path('accountant/', include('accountantapp.urls')),
    # Receptionist routes removed
]
