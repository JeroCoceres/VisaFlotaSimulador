from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from costcenter.models import Cards,Transaction
from costcenter.forms import TransactionForm

@login_required
def index(request):
    all_cards = Cards.objects.all()
    all_transactions = Transaction.objects.all()
    context = {"Cards": all_cards, "transactions":all_transactions}
    return render(request, 'base copy.html', context=context)


