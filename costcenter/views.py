from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from costcenter.forms import TransactionForm
from costcenter.models import Consumo,Transaction,Cards, Distribution
from django.db.models import Sum
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

def transaction_success(request):
    return render(request, 'costcenter/transaction_success.html')

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
    unidad = request.user.userprofile.unit
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
    return render(request, "costcenter/InformacionPorCentroDeCostosAnterior.html", {'form': form, 'unit':unidad})



def InformacionPorCentroDeCostosAnterior_Totales(request, periodo):
    # Imprimir para verificar el periodo recibido
    print(f"Periodo recibido: {periodo}")
    
    # Separar mes y año del periodo
    mes, anio = periodo.split('-')
    mes = int(mes)
    anio = int(anio)
    
    # Obtener todas las tarjetas del usuario logueado
    tarjetas = Cards.objects.filter(user=request.user, is_costcenter=False)
    
    # Obtener la unidad del usuario
    unidad = request.user.userprofile.unit

    # Calcular el saldo inicial como la suma de los saldos de todas las tarjetas al inicio del mes
    saldo_inicial = tarjetas.aggregate(total_saldo=Sum('money')).get('total_saldo') or 0.0

    # Calcular el total de consumos del mes para todas las tarjetas
    total_consumos = Consumo.objects.filter(
        card__in=tarjetas,
        consumo_date__month=mes,
        consumo_date__year=anio
    ).aggregate(total_consumo=Sum('importe')).get('total_consumo') or 0.0

    # Preparar la lista de datos que se enviará al template
    datos_tarjetas = []

    for tarjeta in tarjetas:
        # Calcular saldo inicial para cada tarjeta
        saldo_anterior = tarjeta.money  # Suponiendo que `money` almacena el saldo actual de la tarjeta
        
        # Filtrar transacciones de crédito (entradas de fondos)
        creditos = Transaction.objects.filter(
            to_account=tarjeta,
            movement_date__month=mes,
            movement_date__year=anio
        ).aggregate(total_credito=Sum('amount')).get('total_credito') or 0.0
        
        # Filtrar transacciones de débito (salidas de fondos)
        debitos = Transaction.objects.filter(
            from_account=tarjeta,
            movement_date__month=mes,
            movement_date__year=anio
        ).aggregate(total_debito=Sum('amount')).get('total_debito') or 0.0
        
        # Filtrar consumos en el mes y año dados
        consumos = Consumo.objects.filter(
            card=tarjeta,
            consumo_date__month=mes,
            consumo_date__year=anio
        ).aggregate(total_consumo=Sum('importe')).get('total_consumo') or 0.0

        # Calcular saldo final para el periodo
        saldo_final = saldo_anterior + creditos - debitos - consumos
        
        # Añadir datos al diccionario para cada tarjeta
        datos_tarjetas.append({
            'tarjeta': tarjeta.card_number,
            'denominacion': tarjeta.card_name,
            'cuenta': (tarjeta.card_number // 37200000),  # Asumiendo que este es el cálculo para la cuenta asociada
            'saldo_anterior': saldo_anterior,
            'credito': creditos,
            'debito': debitos,
            'otros': 0.0,  # Si hay alguna otra lógica para calcular 'Otros', agrégala aquí
            'consumos': consumos,
            'saldo': saldo_final,
        })
    
    # Preparar el contexto con los datos estructurados
    context = {
        'datos_tarjetas': datos_tarjetas,
        'periodo': periodo,
        'unidad': unidad,
        'saldo_inicial': saldo_inicial,  # Saldo inicial de todas las tarjetas al comienzo del mes
        'total_consumos': total_consumos,  # Total de consumos del mes para todas las tarjetas
    }
    print(context['unidad'])
    
    return render(request, "costcenter/PeriodoAnterior/Totales_informacion.html", context)

def detalle_tarjeta_mes(request, tarjeta, periodo):
    # Parsear el mes y año desde el periodo
    mes, anio = map(int, periodo.split('-'))
    
    # Obtener la tarjeta específica
    card = get_object_or_404(Cards, card_number=tarjeta, user=request.user)
    
    # Filtrar los consumos de la tarjeta en el mes y año dados
    consumos = Consumo.objects.filter(
        card=card,
        consumo_date__month=mes,
        consumo_date__year=anio
    )

    # Calcular el total de consumos en el periodo
    total_consumo = consumos.aggregate(total=Sum('importe'))['total'] or 0.0

    # Calcular el saldo inicial de la tarjeta al comienzo del mes seleccionado
    # Aquí asumimos que el saldo inicial es el saldo actual de la tarjeta más el total de los consumos del mes
    saldo_inicial = card.money + total_consumo

    # Pasar los datos al template
    context = {
        'card': card,
        'saldo_inicial': saldo_inicial,
        'consumos': consumos,
        'total_consumo': total_consumo,
        'periodo': periodo,
    }
    return render(request, 'costcenter/PeriodoAnterior/detalle_tarjeta_mes.html', context)



def InformacionYMovimientosPorTarjetasAnterior(request):
    form = MesesForm(request.POST or None)

    if request.method == 'POST':
        periodo = request.POST.get('periodo')
        tarjeta = request.POST.get('tarjeta')

        if periodo and tarjeta:
            if '-' in periodo:
                try:
                    mes, anio = map(int, periodo.split('-'))
                    card = Cards.objects.get(card_number=tarjeta, user=request.user)

                    # Verificar que la tarjeta no sea un centro de costos
                    if card.is_costcenter:
                        messages.error(request, "Error, tarjeta inexistente")
                    else:
                        # Redirigir a la vista `detalle_tarjeta_mes` si todo es correcto
                        return redirect(reverse('detalle_tarjeta_mes', kwargs={'tarjeta': card.card_number, 'periodo': f"{mes}-{anio}"}))

                except Cards.DoesNotExist:
                    messages.error(request, "Error, tarjeta inexistente")

                except ValueError:
                    messages.error(request, "Formato de período incorrecto.")
            else:
                messages.error(request, "El formato de período debe ser MM-AAAA.")
        else:
            messages.error(request, "Debe ingresar un período y un número de tarjeta.")
    
    return render(request, "costcenter/InformacionYMovimientosPorTarjetasAnterior.html", {'form': form})








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
