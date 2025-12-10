from django import forms
from .models import Bill, Payment

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['patient_name', 'email', 'amount', 'status']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid', 'method']