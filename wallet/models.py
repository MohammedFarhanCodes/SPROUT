from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    savings_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    investment_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wallet_status = models.BooleanField(default=True)  # active or inactive

    def __str__(self):
        return f"Wallet of {self.user}"

    def add_transaction(self, amount, transaction_type, description=None, account=None):
        Transaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            account=account
        )


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('payment', 'Payment')
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.CharField(max_length=50, blank=True, null=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} to wallet {self.wallet.id} on {self.created_at}"
