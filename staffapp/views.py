from django.views.decorators.cache import never_cache
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from adminapp.models import Notification


# Create your views here.

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def staffhome(req):
    if 'staffid' not in req.session:
        return render(req, 'login.html')
    return render(req, 'staffhome.html')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewnoti(request):
    if 'staffid' not in request.session:
        return redirect('login')
    notifications = Notification.objects.all().order_by('created_at')
    return render(request, 'viewnoti.html', {'notifications': notifications})



@never_cache
def stafflogout(request):
    if 'staffid' in request.session:
        del request.session['staffid']  # or whatever session key you're using
        messages.success(request, "Logout Successful!")
    else:
        messages.info(request, "You were not logged in.")
    return redirect('login')  # redirect to staff login page
