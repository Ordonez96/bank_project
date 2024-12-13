from django.shortcuts import render, redirect
from .models import Account, Transaction
from django.utils.timezone import now
from decimal import Decimal


def home(request):
    account, _ = Account.objects.get_or_create(id=1)
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')
    return render(request, 'bank/home.html', {'account': account, 'transactions': transactions})

def add_transaction(request):
    if request.method == 'POST':
        account = Account.objects.get(id=1)
        transaction_type = request.POST['transaction_type']
        amount = Decimal(request.POST['amount'])  # Convertir a Decimal

        # Verificar si es una retirada y si hay suficientes fondos
        if transaction_type == 'withdrawal' and account.balance < amount:
            # Si no hay fondos suficientes, redirigir a la página de alerta
            return render(request, 'bank/alert.html', {'message': 'Fondos insuficientes para realizar la transacción'})

        # Realizar la transacción
        if transaction_type == 'deposit':
            account.balance += amount
        elif transaction_type == 'withdrawal':
            account.balance -= amount

        account.save()
        Transaction.objects.create(account=account, transaction_type=transaction_type, amount=amount)
        return redirect('home')

    return render(request, 'bank/add_transaction.html')