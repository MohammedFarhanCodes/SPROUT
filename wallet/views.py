from django.shortcuts import render, redirect
from .models import Wallet, Transaction
from decimal import Decimal


# Create your views here.
def wallet_balance(request):
    transactions = Transaction.objects.filter(wallet=request.user.wallet).order_by('-created_at')[:5]
    return render(request, 'wallet/wallet_balance.html', {'transactions': transactions})


def transfer_balance(request):
    if request.method == 'POST':
        f = request.POST.get('from')
        t = request.POST.get('to')
        amount = Decimal(request.POST.get('amount'))
        print(request.POST)
        if f == t:
            return redirect(request.META.get('HTTP_REFERER'))
        wallet = Wallet.objects.get(user=request.user)
        if f == 'savings' and Decimal(amount) <= wallet.savings_balance:
            wallet.savings_balance -= amount
            wallet.investment_balance += amount
            wallet.add_transaction(
                amount=amount,
                transaction_type='Transfer',
                account='Savings -> Current'
            )
        elif f == 'current' and Decimal(amount) <= wallet.investment_balance:
            wallet.investment_balance -= amount
            wallet.savings_balance += amount
            wallet.add_transaction(
                amount=amount,
                transaction_type='Transfer',
                account='Current -> Savings'
            )
        wallet.save()
    return redirect('wallet:wallet_balance')


def transaction_history(request):
    t = Transaction.objects.filter(wallet=request.user.wallet).order_by('-created_at')
    return render(request, 'wallet/transactions.html', {'transactions': t})


def goal(request):
    return render(request, 'wallet/savings goal.html')
