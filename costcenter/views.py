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
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RealizarDistribucion.html",context=context)

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
    return render(request,"costcenter/DevolucionessRealizadas.html",context=context)

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

def MovimientosPorTarjetasPDF(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/MovimientosPorTarjetasPDF.html",context=context)

def MovimientosPorTarjetasXLSX(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/MovimientosPorTarjetasXLSX.html",context=context)

def UltimasLiquidaciones(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/UltimasLiquidaciones.html",context=context)
