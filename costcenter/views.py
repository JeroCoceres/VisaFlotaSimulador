from django.shortcuts import render,redirect
from costcenter.forms import TransactionForm
from costcenter.models import Transaction,Cards
from django.db import transaction

def create_transaction(request):
    if request.method == "GET":
        context = {"form": TransactionForm(), "title": "Nueva transacción"}
        return render(request, "costcenter/new_transaction.html", context=context)
    elif request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data["from_account"]
            to_account = form.cleaned_data["to_account"]
            amount = form.cleaned_data["amount"]

            try:
                with transaction.atomic():
                    from_card = Cards.objects.select_for_update().get(card_name=from_account)
                    to_card = Cards.objects.select_for_update().get(card_name=to_account)

                    if from_card.money >= amount:
                        from_card.money -= amount
                        to_card.money += amount

                        from_card.save()
                        to_card.save()

                        Transaction.objects.create(
                            from_account=from_account,
                            to_account=to_account,
                            amount=amount
                        )

                        return render(request, "costcenter/new_transaction.html", context={"title": "Nueva transacción", "success": True})
                    else:
                        context = {
                            "form_errors": "Saldo insuficiente en la cuenta de origen.",
                            "form": TransactionForm()
                        }
                        return render(request, "costcenter/new_transaction.html", context=context)
            except Cards.DoesNotExist:
                context = {
                    "form_errors": "Una de las cuentas no existe.",
                    "form": TransactionForm()
                }
                return render(request, "costcenter/new_transaction.html", context=context)
        else:
            context = {
                "form_errors": form.errors,
                "form": TransactionForm()
            }
            return render(request, "costcenter/new_transaction.html", context=context)

def show_cards(request):
    non_cost_center_cards = Cards.objects.filter(is_costcenter=False)
    context = {'cards': non_cost_center_cards}
    return render(request, 'costcenter/show_cards.html', context)


def test(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/info_cent_cos3.html",context=context)

def InformacionPorCentroDeCostosActual(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/informacionPorCentroDeCostosActual.html",context=context)

def InformacionYMovimientosPorTarjetasActual(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/InformacionYMovimientosPorTarjetasActual.html",context=context)

def InformacionPorCentroDeCostosAnterior(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/InformacionPorCentroDeCostosAnterior.html",context=context)

def InformacionYMovimientosPorTarjetasAnterior(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/InformacionYMovimientosPorTarjetasAnterior.html",context=context)

def RealizarDistribucionPorOrdenAlfabetico(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RealizarDistribucionPorOrdenAlfabetico.html",context=context)



from django.shortcuts import render, redirect
from .models import Cards, Transaction

def RealizarDistribucion(request):
    if request.method == 'POST':
        # Obtener el centro de costos
        cost_center = Cards.objects.filter(is_costcenter=True).first()
        if not cost_center:
            return render(request, "costcenter/RealizarDistribucion.html", {'error': 'No hay centro de costos disponible.'})
        
        total_amount_to_transfer = 0
        transactions = []
        
        # Recoger y procesar las solicitudes de transferencia
        for key, value in request.POST.items():
            if key.isdigit() and value:
                try:
                    card_number = key
                    amount = float(value)
                    card = Cards.objects.get(card_number=card_number)
                    
                    if amount > 0 and amount <= cost_center.money:
                        total_amount_to_transfer += amount
                        transactions.append((card, amount))
                except (ValueError, Cards.DoesNotExist):
                    continue
        
        # Verificar si el monto total a transferir es válido
        if total_amount_to_transfer <= cost_center.money:
            # Realizar las transacciones y actualizar los saldos
            for card, amount in transactions:
                Transaction.objects.create(from_account=cost_center, to_account=card, amount=amount)
                card.money += amount
                card.save()
                cost_center.money -= amount
            cost_center.save()
        else:
            return render(request, "costcenter/RealizarDistribucion.html", {'error': 'Fondos insuficientes en el centro de costos.'})

        return redirect('realizar_distribucion')

    # Obtener tarjetas de centro de costos y tarjetas no centro de costos
    cost_center_cards = Cards.objects.filter(is_costcenter=True)
    non_cost_center_cards = Cards.objects.filter(is_costcenter=False)
    
    context = {
        'costcenter': cost_center_cards,
        'cards': non_cost_center_cards,
    }
    
    return render(request, "costcenter/RealizarDistribucion.html", context)






def DistribucionesDeFondosRealizadas(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/DistribucionesDeFondosRealizadas.html",context=context)

def RealizarTransferenciasPorOrdenAlfabetico(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RealizarTransferenciasPorOrdenAlfabetico.html",context=context)

def RealizarTransferencias(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RealizarTransferencias.html",context=context)

def TransferenciasRealizadas(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/TransferenciasRealizadas.html",context=context)

def RealizarDevoluciones(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RealizarDevoluciones.html",context=context)

def DevolucionesRealizadas(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/DevolucionesRealizadas.html",context=context)

def AutorizacionesPorTarjetas(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/AutorizacionesPorTarjetas.html",context=context)

def RendicionesPorCentroDeCostosPDF(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RendicionesPorCentroDeCostosPDF.html",context=context)

def RendicionesPorCentroDeCostosXLSX(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RendicionesPorCentroDeCostosXLSX.html",context=context)

def RendicionPorCuentaPDF(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RendicionPorCuentaPDF.html",context=context)

def RendicionPorCuentaXLSX(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RendicionPorCuentaXLSX.html",context=context)

def MovimientosPorTarjetasPDF(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/MovimientosPorTarjetasPDF.html",context=context)

def MovimientosPorTarjetasXLSX(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/MovimientosPorTarjetasXLSX.html",context=context)

def UltimasLiquidaciones(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/UltimasLiquidaciones.html",context=context)
