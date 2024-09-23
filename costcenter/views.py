from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from costcenter.forms import TransactionForm
from costcenter.models import Transaction,Cards, Distribution
from django.contrib import messages
from .forms import MesesForm
from datetime import datetime
from django.urls import reverse

def create_transaction(request):
    if request.method == 'POST':
        # Captura los datos del formulario
        from_account_number = request.POST.get('from_account')
        to_account_number = request.POST.get('to_account')
        amount = float(request.POST.get('amount', 0))
        
        # Validación de que la cuenta de origen esté seleccionada
        if not from_account_number:
            messages.error(request, 'Por favor, seleccione una cuenta de origen.')
            return render(request, 'costcenter/RealizarTransferencias.html')  # Renderiza la vista de formulario de nuevo
        
        try:
            # Obtén las tarjetas basadas en los números de cuenta
            from_card = Cards.objects.get(card_number=from_account_number, user=request.user)
            to_card = Cards.objects.get(card_number=to_account_number)
            
            if from_card.money >= amount:
                # Realiza la transacción
                from_card.money -= amount
                to_card.money += amount
                from_card.save()
                to_card.save()

                # Crea el registro de la transacción
                Transaction.objects.create(
                    user=request.user,
                    from_account=from_card,
                    to_account=to_card,
                    amount=amount,
                )
                print(f"Create Transaction{from_card} ---------- {to_card}")
                return redirect('transaction_success')  # Redirige a una página de éxito
            else:
                messages.error(request, 'Saldo insuficiente en la cuenta de origen.')
        
        except Cards.DoesNotExist:
            messages.error(request, 'Una de las cuentas no existe o no tiene permiso para acceder a ella.')
    
    # Renderiza el formulario si no es POST o si ocurre un error
    form = TransactionForm()
    return render(request, 'costcenter/RealizarTransferencias.html', {'form': form})


def show_cards(request):
    non_cost_center_cards = Cards.objects.filter(is_costcenter=False, user=request.user)
    context = {'cards': non_cost_center_cards}
    print(f"show cards{context}")
    return render(request, 'costcenter/show_cards.html', context)

def get_user_cards_origen(request):
    if request.user.is_authenticated:
        cards = Cards.objects.filter(user=request.user)
        input_field_id_origen = request.GET.get('input_field_id_origen')
        context = {'cards': cards, 'input_field_id_origen': input_field_id_origen}
        print(f"get user cards{context}")
        return render(request, 'costcenter/card_selection_origen.html', context)
    else:
        return JsonResponse({'error': 'No autorizado'}, status=401)

def get_user_cards_destiny(request):
    if request.user.is_authenticated:
        cards = Cards.objects.filter(user=request.user)
        input_field_id_destino = request.GET.get('input_field_id_destino')
        context = {'cards': cards, 'input_field_id_destino': input_field_id_destino}
        print(f"get user cards{context}")
        return render(request, 'costcenter/card_selection_destiny.html', context)
    else:
        return JsonResponse({'error': 'No autorizado'}, status=401)
    



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
    if request.method == 'POST':
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")  # Esto debería aparecer en consola
        print(request.POST)  # Muestra el contenido del POST en la consola
        form = MesesForm(request.POST)
        if form.is_valid():
            periodo = form.cleaned_data['periodo']
            print(f"Periodo válido: {periodo}")  # Esto debería aparecer en consola si el formulario es válido
            # Redirige con el periodo usando guion
            return redirect(reverse('totales_informacion', kwargs={'periodo': periodo}))
        else:
            print("Errores en el formulario:", form.errors)  # Muestra los errores si los hay
    else:
        form = MesesForm()
    return render(request, "costcenter/InformacionPorCentroDeCostosAnterior.html", {'form': form})


def InformacionPorCentroDeCostosAnterior_Totales(request, periodo):
    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    print(f"Periodo recibido: {periodo}")  # Esto te ayudará a verificar si el periodo se pasa correctamente
    # Procesa el periodo como sea necesario
    mes, anio = periodo.split('-')  # Cambia '/' por '-'
    transacciones = Transaction.objects.filter(
        movement_date__month=int(mes), 
        movement_date__year=int(anio)
    )
    context = {
        'transacciones': transacciones,
        'periodo': periodo,
    }
    return render(request, "costcenter/PeriodoAnterior/Totales_informacion.html", context)


# def InformacionPorCentroDeCostosAnterior(request):
#     context= {"test":"Jeronimo"}
#     return render(request,"costcenter/InformacionPorCentroDeCostosAnterior.html",context=context)

def InformacionYMovimientosPorTarjetasAnterior(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/InformacionYMovimientosPorTarjetasAnterior.html",context=context)

def RealizarDistribucionPorOrdenAlfabetico(request):
    context= {"test":"Jeronimo"}
    return render(request,"costcenter/RealizarDistribucionPorOrdenAlfabetico.html",context=context)



def RealizarDistribucion(request):
    if request.method == 'POST':
        # Obtener el centro de costos
        cost_center = Cards.objects.filter(is_costcenter=True).first()
        if not cost_center:
            messages.error(request, 'No hay centro de costos disponible.')
            return redirect('realizar_distribucion')
        
        total_amount_to_transfer = 0
        transactions = []
        
        # Recoger y procesar las solicitudes de transferencia
        for key, value in request.POST.items():
            if key.isdigit() and value:
                try:
                    card_number = key
                    amount = float(value)
                    card = Cards.objects.get(card_number=card_number, user=request.user)
                    
                    if amount > 0 and amount <= cost_center.money:
                        total_amount_to_transfer += amount
                        transactions.append((card, amount))
                    else:
                        messages.error(request, f'Fondos insuficientes para transferir {amount} a la tarjeta {card.card_number}.')
                except (ValueError, Cards.DoesNotExist):
                    continue
        
        # Verificar si el monto total a transferir es válido
        if total_amount_to_transfer <= cost_center.money:
            # Realizar las transacciones y actualizar los saldos
            for card, amount in transactions:
                Distribution.objects.create(from_account=cost_center, to_account=card, amount=amount, user=request.user)
                card.money += amount
                card.save()
                cost_center.money -= amount
            cost_center.save()
        else:
            messages.error(request, 'Fondos insuficientes en el centro de costos.')

        return redirect('realizar_distribucion')

    # Obtener tarjetas de centro de costos y tarjetas no centro de costos
    cost_center_cards = Cards.objects.filter(is_costcenter=True, user=request.user)
    non_cost_center_cards = Cards.objects.filter(is_costcenter=False, user=request.user)
    
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
    cards = Cards.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            from_card = transaction.from_account
            to_card = transaction.to_account
            amount = transaction.amount

            if from_card.money >= amount:
                from_card.money -= amount
                to_card.money += amount
                from_card.save()
                to_card.save()
                transaction.save()
                return redirect('transaction_success')  # Redirect to a success page
            else:
                return render(request, 'costcenter/RealizarTransferencias.html', {'cards': cards, 'form': form, 'error': 'Saldo insuficiente en la cuenta de origen.'})
    else:
        form = TransactionForm()

    context = {
        'cards': cards,
        'form': form,
        'test': "Jeronimo"
    }
    return render(request, 'costcenter/RealizarTransferencias.html', context)

def get_account_balance(request, card_id):
    card = get_object_or_404(Cards, id=card_id)
    data = {
        'previous_balance': card.previous_balance,  # Assuming previous_balance is a field in Cards
        'current_balance': card.money
    }
    return JsonResponse(data)



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
