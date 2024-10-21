from django.shortcuts import render, redirect
from .models import Wallet
from decimal import Decimal


# Create your views here.
def wallet_balance(request):
    return render(request, 'wallet/wallet_balance.html')


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
        elif f == 'current' and Decimal(amount) <= wallet.investment_balance:
            wallet.investment_balance -= amount
            wallet.savings_balance += amount
        wallet.save()
    return redirect('wallet:wallet_balance')


