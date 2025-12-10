from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_control
from .models import Bill, Payment
from .forms import BillForm, PaymentForm
from django.core.mail import send_mail
from django.db import models
from django.views.generic.edit import UpdateView

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def accountant_dashboard(request):
    if not request.session.get('accountant_id'):
        return redirect('login')
    return render(request, 'accountantapp/accountant_dashboard.html')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def accountant_logout(request):
    request.session.flush()
    return redirect('login')

def all_bills(request):
    if not request.session.get('accountant_id'):
        return redirect('login')
    bills = Bill.objects.all()
    return render(request, 'accountantapp/all_bills.html', {'bills': bills})

def payments(request):
    bill_id = request.GET.get('bill_id')
    if bill_id:
        payments = Payment.objects.filter(bill_id=bill_id)
    else:
        payments = Payment.objects.select_related('bill').all()
    total_received = payments.aggregate(total=models.Sum('amount_paid'))['total'] or 0
    return render(request, 'accountantapp/payments.html', {
        'payments': payments,
        'total_received': total_received,
    })

def reports(request):
    # You can add report logic here
    return render(request, 'accountantapp/reports.html')

def billing_history(request):
    bills = Bill.objects.order_by('-date_issued')
    return render(request, 'accountantapp/billing_history.html', {'bills': bills})

def create_bill(request):
    if not request.session.get('accountant_id'):
        return redirect('login')
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save()
            # Only send email if the generate button was clicked
            if 'generate_bill' in request.POST:
                send_mail(
                    subject='Your Hospital Bill',
                    message=f'Dear {bill.patient_name},\n\nYour bill amount is {bill.amount}.\nStatus: {bill.status}\nThank you.',
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL
                    recipient_list=[bill.email],
                    fail_silently=False,
                )
            return redirect('all_bills')
    else:
        form = BillForm()
    return render(request, 'accountantapp/create_bill.html', {'form': form})

def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('all_bills')
    else:
        form = BillForm(instance=bill)
    return render(request, 'accountantapp/create_bill.html', {'form': form, 'edit_mode': True})

def change_bill_status(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == 'POST':
        bill.status = request.POST.get('status')
        bill.save()
    return redirect('all_bills')

def approve_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == 'POST':
        bill.status = 'paid'
        bill.save()
    return redirect('all_bills')

def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if request.method == 'POST':
        bill.delete()
    return redirect('all_bills')

def make_payment(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if bill.status == 'paid':
        return redirect('all_bills')
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.bill = bill
            payment.save()
            bill.status = 'paid'
            bill.save()
            return redirect('payments')
    else:
        form = PaymentForm(initial={'amount_paid': bill.amount})
    return render(request, 'accountantapp/make_payment.html', {'form': form, 'bill': bill})

class EditPaymentView(UpdateView):
    model = Payment
    fields = ['amount_paid', 'method']  # Remove 'payment_date'
    template_name = 'accountantapp/edit_payment.html'
    success_url = '/accountant/payments/'
