from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.core.mail import send_mail
from mainapp.models import DoctorRegister, Appointment
from adminapp.models import Notification

# Helper function to check if doctor is logged in
def is_doctor_logged_in(request):
    return 'doctor_id' in request.session

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def doctorhome(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        messages.error(request, "Please log in as a doctor.")
        return redirect('login')

    try:
        doctor = DoctorRegister.objects.get(doctor_id=doctor_id)
    except DoctorRegister.DoesNotExist:
        messages.error(request, "Doctor not found.")
        return redirect('login')

    # Only show appointments for this doctor
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctorhome.html', {
        'doctor': doctor,
        'appointments': appointments
    })


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def vpa(request):
    if not is_doctor_logged_in(request):
        return redirect('login')
    doctor_id = request.session.get('doctor_id')
    doctor = DoctorRegister.objects.get(doctor_id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('appointment_date', 'appointment_time')
    return render(request, 'vpa.html', {'appointments': appointments, 'doctor': doctor})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def markaproove(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.is_completed = True
    appointment.save()

    # Generate bill if not already created
    from adminapp.models import Bill
    if not Bill.objects.filter(appointment=appointment).exists():
        Bill.objects.create(
            appointment=appointment,
            amount=500,  # Set your default or calculated amount here
            description="Consultation charges"
        )

    # Email content
    subject = 'Appointment Confirmation'
    message = f"""
Dear {appointment.name},

Your appointment with Dr. {appointment.doctor.doctor_name} ({appointment.doctor_speciality}) 
has been approved for {appointment.appointment_date} at {appointment.appointment_time}.
Thank you for choosing MediConnect!
"""
    recipient = appointment.email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='teammediconnect@gmail.com',
            recipient_list=[recipient],
            fail_silently=False,
        )
        messages.success(request, f"Appointment approved and email sent to {recipient}.")
    except Exception as e:
        messages.warning(request, "Appointment approved, but email failed to send.")

    return redirect('doctorapp:vpa')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deleteappointment(request, id):
    if not is_doctor_logged_in(request):
        return redirect('login')
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect('doctorapp:vpa')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def doctorlogout(request):
    request.session.flush()
    return redirect('login')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def vnoti(request):
    if not is_doctor_logged_in(request):
        return redirect('login')
    notifications = Notification.objects.all().order_by('created_at')
    return render(request, 'vnoti.html', {'notifications': notifications})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def reschedule_appointment(request, app_id):
    if not is_doctor_logged_in(request):
        return redirect('login')
    app = get_object_or_404(Appointment, id=app_id)
    if request.method == 'POST':
        new_date = request.POST.get('appointment_date')
        new_time = request.POST.get('appointment_time')
        app.appointment_date = new_date
        app.appointment_time = new_time
        app.is_completed = True
        app.save()
        # Send email
        send_mail(
            'Your Appointment Has Been Rescheduled',
            f'Hello {app.name},\n\nYour appointment has been rescheduled to {new_date} at {new_time}.\n\nThank you.',
            'teammediconnect@gmail.com',
            [app.email],
            fail_silently=False,
        )
        return redirect('doctorapp:vpa')
    return redirect('doctorapp:vpa')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def profile(request):
    if not is_doctor_logged_in(request):
        return redirect('login')
    doctor_id = request.session.get('doctor_id')
    doctor = DoctorRegister.objects.get(doctor_id=doctor_id)
    return render(request, 'profile.html', {'doctor': doctor})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def edit_profile(request):
    if not is_doctor_logged_in(request):
        return redirect('login')
    doctor_id = request.session.get('doctor_id')
    doctor = DoctorRegister.objects.get(doctor_id=doctor_id)
    if request.method == 'POST':
        doctor.doctor_name = request.POST.get('doctor_name')
        doctor.doctor_email = request.POST.get('doctor_email')
        doctor.doctor_phone = request.POST.get('doctor_phone')
        doctor.experience = request.POST.get('experience')
        doctor.qualification = request.POST.get('qualification')
        doctor.doctors_speciality = request.POST.get('doctors_speciality')
        doctor.address = request.POST.get('address')
        doctor.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('doctorapp:profile')
    return render(request, 'edit_profile.html', {'doctor': doctor})
