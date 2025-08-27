from django import forms
from .models import BankAccount

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

class TransferForm(forms.Form):
    receiver_username = forms.CharField(max_length=150)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
