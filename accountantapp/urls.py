from django.urls import path
from . import views
from .views import EditPaymentView

urlpatterns = [
    path('dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('bills/', views.all_bills, name='all_bills'),
    path('bills/create/', views.create_bill, name='create_bill'),
    path('payments/', views.payments, name='payments'),
    path('reports/', views.reports, name='reports'),
    path('billing-history/', views.billing_history, name='billing_history'),
    path('bills/<int:bill_id>/edit/', views.edit_bill, name='edit_bill'),
    path('bills/<int:bill_id>/change_status/', views.change_bill_status, name='change_bill_status'),
    path('bills/<int:bill_id>/approve/', views.approve_bill, name='approve_bill'),
    path('bills/<int:bill_id>/delete/', views.delete_bill, name='delete_bill'),
    path('bills/<int:bill_id>/pay/', views.make_payment, name='make_payment'),
    path('payments/edit/<int:pk>/', EditPaymentView.as_view(), name='edit_payment'),
]