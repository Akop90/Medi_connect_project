from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mainapp.models import AccountantRequest, AccountantRegister, Complaints
from django.core.mail import send_mail
from .models import Bill
from django.views.decorators.http import require_POST

# Admin login required check
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def adminhome(req):
    if 'adminid' not in req.session:
        return redirect('login')
    return render(req, 'adminhome.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def adminlogout(req):
    req.session.flush()
    return redirect('login')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewstaffrequest(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    stf = StaffRequest.objects.all()
    return render(req, 'viewstaffrequest.html', {'stf': stf})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewstaff(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    staff = StaffRegister.objects.all().order_by('-created_at')
    return render(req, 'viewstaff.html', {'staff': staff})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deletestaff(req, id):
    if not req.session.get('adminid'):
        return redirect('login')  # or your custom login page
    staff = get_object_or_404(StaffRegister, id=id)
    staff.delete()
    return redirect('adminapp:viewstaff')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def acceptstaffrequest(req, id):
    if 'adminid' not in req.session:
        return redirect('login')

    # Fetch the request
    staff_req = get_object_or_404(StaffRequest, id=id)

    # Save to StaffRegister
    staff = StaffRegister.objects.create(
        staff_name=staff_req.staff_name,
        staff_email=staff_req.staff_email,
        staff_password=staff_req.staff_password,
        staff_phone=staff_req.staff_phone,
        staff_address=staff_req.staff_address,
    )

    # Prepare email content
    subject = 'Staff Registration Approved'
    message = f"""
    Dear {staff.staff_name},

    Your staff registration at MediConnect has been successfully approved.

    You can now log in and begin using our system with the email you registered.

    Thank you for joining MediConnect!
    """
    recipient = staff.staff_email

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='teammediconnect@gmail.com',  # Your Gmail address
            recipient_list=[recipient],
            fail_silently=False,
        )
        messages.success(req, f"Staff approved and email sent to {recipient}.")
    except Exception as e:
        messages.warning(req, "Staff approved, but email could not be sent. Please check your email settings.")

    # Delete the request after approval
    staff_req.delete()
    return redirect('adminapp:viewstaffrequest')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deletestaffrequest(req, id):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    StaffRequest.objects.filter(id=id).delete()
    return redirect('adminapp:viewstaffrequest')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def addstaff(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    if req.method == 'POST':
        staff_name = req.POST.get('staff_name')
        staff_email = req.POST.get('staff_email')
        staff_password = req.POST.get('staff_password')
        staff_phone = req.POST.get('staff_phone')
        staff_address = req.POST.get('staff_address')

        staff = StaffRegister(
            staff_name=staff_name,
            staff_email=staff_email,
            staff_password=staff_password,
            staff_phone=staff_phone,
            staff_address=staff_address
        )
        staff.save()
        
        return redirect('adminapp:viewstaff')

    prefill = req.GET
    return render(req, 'addstaff.html', {'prefill': prefill})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewdoctorrequest(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    dct = DoctorRequest.objects.all()
    return render(req, 'viewdoctorrequest.html', {'dct': dct})



@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def adddoctor(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    specialities = [
        'General Physician',
        'Obstetrician/Gynecologist (OB/GYN)',
        'Pediatrician',
        'Cardiologist',
        'Orthopaedics'
    ]

    if req.method == 'POST':
        doctor_id = req.POST.get('doctor_id')
        doctor_name = req.POST.get('doctor_name')
        doctors_speciality = req.POST.get('doctors_speciality')
        doctor_email = req.POST.get('doctor_email')
        doctor_password = req.POST.get('doctor_password')
        doctor_phone = req.POST.get('doctor_phone')

        # Create approved doctor entry
        DoctorRegister.objects.create(
            doctor_id=doctor_id,
            doctor_name=doctor_name,
            doctors_speciality=doctors_speciality,
            doctor_email=doctor_email,
            doctor_phone=doctor_phone,
            doctor_password=doctor_password
        )

        return redirect('adminapp:viewdoctor')

    prefill = req.GET
    return render(req, 'adddoctor.html', {
        'prefill': prefill,
        'specialities': specialities
    })


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def acceptdoctorrequest(req, id):
    if 'adminid' not in req.session:
        return redirect('login')

    # Fetch the doctor request
    doc_req = get_object_or_404(DoctorRequest, id=id)

    # Save to DoctorRegister
    doctor = DoctorRegister.objects.create(
        doctor_id=doc_req.doctor_id,
        doctor_name=doc_req.doctor_name,
        doctors_speciality=doc_req.doctors_speciality,
        doctor_email=doc_req.doctor_email,
        doctor_phone=doc_req.doctor_phone,
        doctor_password=doc_req.doctor_password
    )

    # Prepare email content
    subject = 'Doctor Registration Approved'
    message = f"""
    Dear Dr. {doctor.doctor_name},

    Your registration as a {doctor.doctors_speciality} at MediConnect has been successfully approved.

    You can now log in and begin managing your appointments using the email you registered with.

    Thank you for being a part of MediConnect!
    """
    recipient = doctor.doctor_email

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='teammediconnect@gmail.com',  # Replace with your verified Gmail
            recipient_list=[recipient],
            fail_silently=False,
        )
        messages.success(req, f"Doctor approved and email sent to {recipient}.")
    except Exception as e:
        messages.warning(req, "Doctor approved, but email could not be sent. Please check your email settings.")

    # Delete request after processing
    doc_req.delete()
    return redirect('adminapp:viewdoctorrequest')


def deletedoctorrequest(req, id):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    DoctorRequest.objects.filter(id=id).delete()
    return redirect('adminapp:viewdoctorrequest')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewdoctor(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    doctors = DoctorRegister.objects.all().order_by('created_at')
    return render(req, 'viewdoctor.html', {'doctors': doctors})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def dkp(req, doctor_id):
    if not req.session.get('adminid'):
        return redirect('login')  # custom admin login page

    doctor = get_object_or_404(DoctorRegister, doctor_id=doctor_id)
    doctor.delete()
    return redirect('adminapp:viewdoctor')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewcomplaints(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    complaints = Complaints.objects.all().order_by('registered_date')
    return render(req, 'viewcomplaints.html', {'complaints': complaints})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deletecomplaint(req, id):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    complaint = get_object_or_404(Complaints, id=id)
    complaint.delete()
    return redirect('adminapp:viewcomplaints')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def addnotification(request):
    if 'adminid' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        message = request.POST.get('message')
        send_to_list = request.POST.getlist('send_to')

        if not send_to_list:
            messages.warning(request, "Please select at least one recipient (Staff or Doctor).")
            return render(request, 'addnotification.html', {'message': message})

        for recipient in send_to_list:
            Notification.objects.create(
                message=message,
                send_to=recipient
            )
        messages.success(request, "Notification(s) sent successfully.")
        return redirect('adminapp:viewnotifi')

    return render(request, 'addnotification.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewnotifi(request):
    if 'adminid' not in request.session:
        return redirect('login')
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'viewnotifi.html', {'notifications': notifications})
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deletenotification(request, id):
    if 'adminid' not in request.session:
        return redirect('login')
    Notification.objects.filter(id=id).delete()
    return redirect('adminapp:viewnotifi')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def billing(request):
    if 'adminid' not in request.session:
        return redirect('login')
    bills = Bill.objects.select_related('appointment').all().order_by('-created_at')
    return render(request, 'billing.html', {'bills': bills})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def create_bill(request, appointment_id):
    if 'adminid' not in request.session:
        return redirect('login')
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')
        # Prevent duplicate bills for the same appointment
        if Bill.objects.filter(appointment=appointment).exists():
            messages.warning(request, "Bill already exists for this appointment.")
            return redirect('adminapp:billing')
        Bill.objects.create(
            appointment=appointment,
            amount=amount,
            description=description
        )
        # Optionally send email here
        messages.success(request, "Bill created and sent to patient.")
        return redirect('adminapp:billing')
    return render(request, 'create_bill.html', {'appointment': appointment})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def mark_bill_paid(request, bill_id):
    if 'adminid' not in request.session:
        return redirect('login')
    bill = get_object_or_404(Bill, id=bill_id)
    bill.is_paid = True
    bill.save()
    messages.success(request, "Bill marked as paid.")
    return redirect('adminapp:billing')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def view_accountant_requests(request):
    if 'adminid' not in request.session:
        return redirect('login')
    requests = AccountantRequest.objects.all()
    return render(request, 'adminapp/view_accountant_requests.html', {'requests': requests})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def approve_accountant(request, req_id):
    if 'adminid' not in request.session:
        return redirect('login')
    req = get_object_or_404(AccountantRequest, id=req_id)
    accountant = AccountantRegister.objects.create(
        name=req.name,
        email=req.email,
        password=req.password,
        phone=req.phone,
        address=req.address
    )

    # Prepare email content
    subject = 'Accountant Registration Approved'
    message = f"""
    Dear {accountant.name},

    Your accountant registration at MediConnect has been approved.

    You can now log in and begin using our system with the email you registered.

    Thank you for joining MediConnect!
    """
    recipient = accountant.email

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='teammediconnect@gmail.com',  # Use your verified sender email
            recipient_list=[recipient],
            fail_silently=False,
        )
        messages.success(request, f"Accountant approved and email sent to {recipient}.")
    except Exception as e:
        messages.warning(request, "Accountant approved, but email could not be sent. Please check your email settings.")

    req.delete()
    return redirect('adminapp:view_accountant_requests')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def decline_accountant(request, req_id):
    if 'adminid' not in request.session:
        return redirect('login')
    req = get_object_or_404(AccountantRequest, id=req_id)
    req.delete()
    messages.info(request, "Accountant request declined.")
    return redirect('adminapp:view_accountant_requests')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def view_accountants(request):
    if 'adminid' not in request.session:
        return redirect('login')
    accountants = AccountantRegister.objects.all()
    return render(request, 'adminapp/view_accountants.html', {'accountants': accountants})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def delete_accountant(request, acc_id):
    if 'adminid' not in request.session:
        return redirect('login')
    acc = get_object_or_404(AccountantRegister, id=acc_id)
    acc.delete()
    messages.success(request, "Accountant deleted.")
    return redirect('adminapp:view_accountants')
# Receptionist-related admin views removed (model and app deleted).
# If you need to re-enable receptionist admin functionality, re-implement these views
# using the new model or restore the model/migrations from backup.