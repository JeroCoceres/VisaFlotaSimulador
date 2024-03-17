from django.shortcuts import render
from costcenter.forms import TransactionForm
from costcenter.models import Transaction,Cards


def create_transaction(request):
    if request.method == "GET":
        context = {"form" : TransactionForm(),"title": "Nueva transacción"}
        return render(request,"costcenter/new_transaction.html",context=context)
    elif request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            Transaction.objects.create(
            from_account = form.cleaned_data["from_account"],
            to_account = form.cleaned_data["to_account"],
            movement = form.cleaned_data["movement"],
            movement_date = form.cleaned_data["movement_date"],
            amount = form.cleaned_data["amount"]
            
            )
            def new_transaction():
                account_to_modify = Cards.objects.get(card_name = form.cleaned_data["to_account"])
                account_to_modify.money += form.cleaned_data["amount"]
                account_to_modify.save()
                account_from_modify = Cards.objects.get(card_name = form.cleaned_data["from_account"])
                account_from_modify.money -= form.cleaned_data["amount"]
                account_from_modify.save()

            new_transaction()
            return render(request,"costcenter/new_transaction.html",context={})
        else:
            context = {
                "form_errors": form.errors,
                "form":TransactionForm()
            }
            return render(request,"costcenter/new_transaction.html",context=context)

def test(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/info_cent_cos3.html",context=context)
