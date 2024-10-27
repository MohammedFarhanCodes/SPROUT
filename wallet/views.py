from django.shortcuts import render, redirect
from .models import Wallet, Transaction, SavingsGoal
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
    if request.method == "POST":
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        wallet = Wallet.objects.get(user=request.user)
        wallet.add_goal(name, amount)
        return redirect('wallet:savings_goal')
    Wallet.objects.get(user=request.user).generate_goal_percentage()
    return render(request, 'wallet/savings goal.html')


def delete_goal(request, goal_id):
    target_goal = SavingsGoal.objects.get(wallet__user=request.user, id=goal_id)
    target_goal.delete()
    return redirect('wallet:savings_goal')


def goal_priority(request, goal_priority, down=False):
    wallet = Wallet.objects.get(user=request.user)
    wallet.change_goal_priority(goal_priority, down)

    return redirect('wallet:savings_goal')


def lock_goal(request, goal_id):
    g = SavingsGoal.objects.get(id=goal_id, wallet__user=request.user)
    g.is_locked = True
    g.save()
    return redirect('wallet:savings_goal')


def unlock_goal(request, goal_id):
    g = SavingsGoal.objects.get(id=goal_id, wallet__user=request.user)
    g.is_locked = False
    g.save()
    return redirect('wallet:savings_goal')
