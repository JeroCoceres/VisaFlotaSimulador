from django.shortcuts import render
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

def RealizarDistribucion(request):


    def show_costcenter():
        cost_center = Cards.objects.filter(is_costcenter=True)
        context1 = {'costcenter': cost_center}
        return context1
    
        

    # Llama a la función interna y almacena el contexto

    def show_cards():
        non_cost_center_cards = Cards.objects.filter(is_costcenter=False)
        context2 = {'cards': non_cost_center_cards}
        return context2

    context = show_cards()
    context = show_costcenter()
    context.update(show_cards())

    return render(request,"costcenter/RealizarDistribucion.html",context)

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
