from django.db import models

# Create your models here.

class Bill(models.Model):
    patient_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)  # <-- Add this line
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])

    def __str__(self):
        return f"{self.patient_name} - {self.amount}"

class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
    ]
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES)

    def __str__(self):
        return f"Payment for {self.bill.patient_name} on {self.payment_date}"


