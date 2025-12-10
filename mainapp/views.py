from django.shortcuts import render,redirect
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import *
from adminapp.models import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def index(req):
    return render(req, 'index.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def login(req):
    if req.method == "POST":
        usertype = req.POST['usertype']
        userid = req.POST['userid']
        password = req.POST['password']
        
        try:
            if usertype == "admin":
                user = AdminLogin.objects.get(userid=userid, password=password)
                req.session['adminid'] = userid
                return redirect('adminapp:adminhome')

            elif usertype == "staff":
                user = StaffRegister.objects.get(staff_email=userid, staff_password=password)
                req.session['staffid'] = userid
                return redirect('staffapp:staffhome')

            elif usertype == "doctor":
                user = DoctorRegister.objects.get(doctor_email=userid, doctor_password=password)
                req.session['doctor_id'] = user.doctor_id  # Store the actual doctor_id, not email
                return redirect('doctorapp:doctorhome')

            elif usertype == "accountant":
                user = AccountantRegister.objects.get(email=userid, password=password)
                req.session['accountant_id'] = userid
                return redirect('accountant_dashboard')

            else:
                return render(req, 'login.html', {"msg": "Invalid usertype selected"})
        except ObjectDoesNotExist:
            messages.error(req, "Invalid credentials.")

    return render(req, 'login.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def staffregister(req):
    if req.method == 'POST':
        staff_name = req.POST.get('staff_name')
        staff_email = req.POST.get('staff_email')
        staff_password = req.POST.get('staff_password')
        staff_phone = req.POST.get('staff_phone')
        staff_address = req.POST.get('staff_address')

        if StaffRegister.objects.filter(staff_email=staff_email).exists() or StaffRequest.objects.filter(staff_email=staff_email).exists():
            messages.error(req, 'This email is already registered or pending approval or already exist')
            return redirect('staffregister')

        staff_req = StaffRequest(
            staff_name=staff_name,
            staff_email=staff_email,
            staff_password=staff_password,
            staff_phone=staff_phone,
            staff_address=staff_address
        )
        staff_req.save()
        messages.success(req, 'Your request has been submitted and is pending approval.You Will be Notified by Email')
        return redirect('staffregister')  

    return render(req, 'staffregistor.html')
    
    
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def aboutus(req):
    return render(req, 'aboutus.html')
    


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def cashless_part(req):
    return render(req, 'cashless_part.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def doctors(req):
    return render(req, 'doctors.html')   



@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def facilities(req):
    return render(req, 'facilities.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def doctorregister(req):
    if req.method == 'POST':
        doctor_id = req.POST.get('doctor_id')
        doctor_name = req.POST.get('doctor_name')
        doctors_speciality = req.POST.get('doctor_speciality')
        doctor_email = req.POST.get('doctor_email')
        doctor_password = req.POST.get('doctor_password')
        doctor_phone = req.POST.get('doctor_phone')

        if DoctorRegister.objects.filter(doctor_email=doctor_email).exists() or DoctorRequest.objects.filter(doctor_email=doctor_email).exists():
            messages.error(req, 'This email is already registered or pending approval.')
            return redirect('doctorregister')

        doctor_req = DoctorRequest(
            doctor_id=doctor_id,
            doctor_name=doctor_name,
            doctors_speciality=doctors_speciality,
            doctor_email=doctor_email,
            doctor_password=doctor_password,
            doctor_phone=doctor_phone
        )
        doctor_req.save()
        messages.success(req, 'Your request has been submitted and is pending approval.You will be notified by Email')
        return redirect('doctorregister')  

    return render(req, 'doctorregister.html')


def gallery(req):
    return render(req, 'gallery.html')





@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def contact(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        phone = req.POST.get('phone')
        complaint = req.POST.get('complaint')

        Complaints.objects.create(
            name=name,
            email=email,
            phone=phone,
            complaint=complaint,
            registered_date=timezone.now().date()
        )

        messages.success(req, 'Your complaint has been submitted successfully.')
        return redirect('contact')

    return render(req, 'contact.html')



@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def mkap(request):
    specialities = [
        'General Physician',
        'Obstetrician/Gynecologist (OB/GYN)',
        'Pediatrician',
        'Cardiologist',
        'Orthopaedics'
    ]

    # This block reloads doctors dropdown when user selects speciality
    selected_speciality = request.GET.get('doctor_speciality') or request.POST.get('doctor_speciality')
    doctors = DoctorRegister.objects.filter(doctors_speciality=selected_speciality) if selected_speciality else []

    # This block only runs when actual form is submitted
    if request.method == 'POST' and request.POST.get('doctor'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        symptoms = request.POST.get('symptoms')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        doctor_speciality = request.POST.get('doctor_speciality')
        doctor_id = request.POST.get('doctor')

        try:
            doctor = DoctorRegister.objects.get(doctor_id=doctor_id)
        except DoctorRegister.DoesNotExist:
            messages.error(request, "Invalid doctor selected. Please try again.")
            return redirect('mkap')

        Appointment.objects.create(
            name=name,
            email=email,
            contact=contact,
            symptoms=symptoms,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            doctor_speciality=doctor_speciality,
            doctor=doctor
        )

        messages.success(request, "Your appointment has been booked successfully.You will be notified by Email")
        return redirect('mkap')

    return render(request, 'mkap.html', {
        'specialities': specialities,
        'selected_speciality': selected_speciality,
        'doctors': doctors
    })


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def accountantregister(req):
    if req.method == 'POST':
        accountant_id = req.POST.get('accountant_id')
        name = req.POST.get('name')
        email = req.POST.get('email')
        password = req.POST.get('password')
        phone = req.POST.get('phone')
        address = req.POST.get('address')

        # Use correct field names as per your models
        if AccountantRegister.objects.filter(email=email).exists() or AccountantRequest.objects.filter(email=email).exists():
            messages.error(req, 'This email is already registered or pending approval.')
            return redirect('accountantregister')

        accountant_req = AccountantRequest(
            name=name,
            email=email,
            password=password,
            phone=phone,
            address=address
        )
        accountant_req.save()
        messages.success(req, 'Your request has been submitted and is pending approval. You will be notified by Email.')
        return redirect('accountantregister')

    return render(req, 'accountantregister.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def accountant_login(req):
    if req.method == "POST":
        email = req.POST.get('userid')
        password = req.POST.get('password')
        try:
            user = AccountantRegister.objects.get(email=email, password=password)
            req.session['accountant_id'] = email
            return redirect('accountantapp:accounthome')
        except AccountantRegister.DoesNotExist:
            messages.error(req, "Invalid credentials.")
    return render(req, 'login.html', {'usertype': 'accountant'})

# Example accountant home view (after login)
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def accounthome(req):
    if not req.session.get('accountant_id'):
        return redirect('login')
    return render(req, 'accountanthome.html')

# Receptionist views removed.

# def test_email(request):
#     send_mail(
#         'Test Email',
#         'This is a test email from Django.',
#         'mediconnect7781@gmail.com',
#         ['ayushhkumar7018@gmail.com'],
#         fail_silently=False,
#     )
#     messages.success(request, 'Test email sent!')
#     return redirect('home')





