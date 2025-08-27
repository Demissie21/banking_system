from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("Deposit", "Deposit"),
        ("Withdrawal", "Withdrawal"),
        ("Transfer", "Transfer"),
    )
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pin = models.CharField(max_length=128)  # hashed PIN

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin)

    def __str__(self):
        return f"{self.user.username}'s Account"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions', null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions', null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.title()} - {self.amount}"
