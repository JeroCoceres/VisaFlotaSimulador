from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from costcenter.forms import TransactionForm
from costcenter.models import Consumo,Transaction,Cards, Distribution
from django.db.models import Sum
from django.contrib import messages
from .forms import MesesForm, ConsumoForm
from datetime import datetime, timedelta
from django.urls import reverse
import json
from django.utils import timezone
from django.http import HttpResponse

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
    unidad = request.user.userprofile.unit
    if request.method == 'POST':
        # Redirige a la nueva vista para mostrar la información del período actual
        return redirect('totales_informacion_actual')

    # Renderiza la página de selección de centro de costos para el período actual
    return render(request, "costcenter/InformacionPorCentroDeCostosActual.html", {'unidad':unidad})



def totales_informacion_actual(request):
    # Obtener la unidad del usuario logueado
    unidad = request.user.userprofile.unit

    # Establecer la fecha de inicio del mes actual
    fecha_inicio_mes_actual = timezone.now().replace(day=1)

    tarjeta_costcenter = Cards.objects.filter(user=request.user, is_costcenter=True).first()

    # Si existe una tarjeta de tipo centro de costos, tomar su número
    costcenter_number = tarjeta_costcenter.card_number if tarjeta_costcenter else "No asignado"


    # Filtrar las tarjetas que no son de centro de costos
    tarjetas = Cards.objects.filter(user=request.user, is_costcenter=False)

    datos_tarjetas = []
    total_consumos = 0
    total_creditos = 0
    total_debitos = 0
    saldo_inicial_total = 0  # Variable para la suma de los saldos iniciales

    for tarjeta in tarjetas:
        # Obtener el saldo actual de la tarjeta
        saldo_actual = tarjeta.money

        # Calcular los consumos del mes actual
        consumos_mes_actual = Consumo.objects.filter(
            card=tarjeta,
            consumo_date__gte=fecha_inicio_mes_actual,
            consumo_date__lte=timezone.now()
        ).aggregate(total=Sum('importe'))['total'] or 0.0
        total_consumos += consumos_mes_actual

        # Calcular los créditos (transferencias hacia la tarjeta) del mes actual
        creditos_mes_actual = Transaction.objects.filter(
            to_account=tarjeta,
            movement_date__gte=fecha_inicio_mes_actual,
            movement_date__lte=timezone.now()
        ).aggregate(total=Sum('amount'))['total'] or 0.0
        total_creditos += creditos_mes_actual

        # Calcular los débitos (transferencias desde la tarjeta) del mes actual
        debitos_mes_actual = Transaction.objects.filter(
            from_account=tarjeta,
            movement_date__gte=fecha_inicio_mes_actual,
            movement_date__lte=timezone.now()
        ).aggregate(total=Sum('amount'))['total'] or 0.0
        total_debitos += debitos_mes_actual

        # Calcular el saldo anterior sumando los débitos y restando los créditos al saldo actual
        saldo_anterior = saldo_actual + debitos_mes_actual + consumos_mes_actual - creditos_mes_actual
        saldo_inicial_total += saldo_anterior  # Sumar el saldo anterior al total

        # Preparar los datos de cada tarjeta
        datos_tarjetas.append({
            'tarjeta': tarjeta.card_number,
            'denominacion': tarjeta.card_name,
            'cuenta': (tarjeta.card_number// 37200000),
            'saldo_anterior': saldo_anterior,
            'credito': creditos_mes_actual,
            'debito': debitos_mes_actual + consumos_mes_actual,
            'acredit': creditos_mes_actual,
            'otros': 0,  # Puedes agregar lógica adicional si es necesario
            'extracciones': debitos_mes_actual,
            'consumos': consumos_mes_actual,
            'saldo': saldo_actual
        })

    # Pasar los datos al contexto
    context = {
        'cc_number':costcenter_number,
        'unidad': unidad,
        'periodo': fecha_inicio_mes_actual.strftime("%m-%Y"),
        'datos_tarjetas': datos_tarjetas,
        'total_consumos': total_consumos,
        'total_creditos': total_creditos,
        'total_debitos': total_debitos,
        'saldo_inicial_total': saldo_inicial_total,  # Agregar el saldo inicial total al contexto
    }

    return render(request, 'costcenter/PeriodoActual/Totales_informacion.html', context)




def InformacionYMovimientosPorTarjetasActual(request):
    unidad = request.user.userprofile.unit
    if request.method == 'POST':
        tarjeta = request.POST.get('tarjeta')
        
        if tarjeta:
            try:
                # Verificar que la tarjeta exista y pertenezca al usuario actual
                card = Cards.objects.get(card_number=tarjeta, user=request.user, is_costcenter=False)
                today = timezone.now()
                mes = today.month
                anio = today.year

                # Redirigir a `detalle_tarjeta_mes` con los parámetros de tarjeta y mes actual
                return redirect(reverse('detalle_tarjeta_mes', kwargs={'tarjeta': card.card_number, 'periodo': f"{mes}-{anio}"}))
            
            except Cards.DoesNotExist:
                messages.error(request, "Error, tarjeta inexistente")
        else:
            messages.error(request, "Debe ingresar un número de tarjeta.")
    
    return render(request, "costcenter/InformacionYMovimientosPorTarjetasActual.html",{'unidad':unidad})








def InformacionPorCentroDeCostosAnterior(request):
    unidad = request.user.userprofile.unit
    if request.method == 'POST':
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
    return render(request, "costcenter/InformacionPorCentroDeCostosAnterior.html", {'form': form, 'unit': unidad})





def InformacionPorCentroDeCostosAnterior_Totales(request, periodo):
    # Parsear el periodo (mes y año)
    mes, anio = map(int, periodo.split('-'))
    # Crear fecha límite para el fin del mes usando zona horaria
    fecha_limite = timezone.make_aware(datetime(anio, mes, 1))
    fecha_fin_mes = (fecha_limite + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Obtener todas las tarjetas del usuario logueado
    tarjetas = Cards.objects.filter(user=request.user, is_costcenter=False)
    unidad = request.user.userprofile.unit
    datos_tarjetas = []

    # Verificar si el periodo solicitado es el periodo actual
    ahora = timezone.now()
    es_periodo_actual = (anio == ahora.year and mes == ahora.month)

    for tarjeta in tarjetas:
        saldo_actual = tarjeta.money  # Asumimos inicialmente que el saldo actual es el saldo de la tarjeta

        # Si estamos en un periodo anterior al actual, ajustamos el saldo actual en función de movimientos posteriores
        if not es_periodo_actual:
            # Movimientos posteriores al mes en análisis
            creditos_posteriores = Transaction.objects.filter(
                to_account=tarjeta,
                movement_date__gt=fecha_fin_mes
            ).aggregate(total_credito=Sum('amount'))['total_credito'] or 0.0

            debitos_posteriores = Transaction.objects.filter(
                from_account=tarjeta,
                movement_date__gt=fecha_fin_mes
            ).aggregate(total_debito=Sum('amount'))['total_debito'] or 0.0

            consumos_posteriores = Consumo.objects.filter(
                card=tarjeta,
                consumo_date__gt=fecha_fin_mes
            ).aggregate(total_consumo=Sum('importe'))['total_consumo'] or 0.0

            # Ajustar saldo actual para reflejar el saldo a fin de mes en el periodo anterior
            saldo_actual = tarjeta.money - creditos_posteriores + debitos_posteriores + consumos_posteriores

        # Movimientos específicos del mes en análisis
        creditos_mes_actual = Transaction.objects.filter(
            to_account=tarjeta,
            movement_date__year=anio,
            movement_date__month=mes
        ).aggregate(total_credito=Sum('amount'))['total_credito'] or 0.0

        debitos_mes_actual = Transaction.objects.filter(
            from_account=tarjeta,
            movement_date__year=anio,
            movement_date__month=mes
        ).aggregate(total_debito=Sum('amount'))['total_debito'] or 0.0

        consumos_mes_actual = Consumo.objects.filter(
            card=tarjeta,
            consumo_date__year=anio,
            consumo_date__month=mes
        ).aggregate(total_consumo=Sum('importe'))['total_consumo'] or 0.0

        # Calcula el saldo inicial en función del saldo final ajustado y los movimientos del mes
        saldo_inicial = saldo_actual + debitos_mes_actual + consumos_mes_actual - creditos_mes_actual

        # Añadir datos al diccionario para cada tarjeta
        datos_tarjetas.append({
            'tarjeta': tarjeta.card_number,
            'denominacion': tarjeta.card_name,
            'cuenta': (tarjeta.card_number // 37200000),  # Cálculo para la cuenta asociada
            'saldo_anterior': saldo_inicial,  # Saldo inicial calculado
            'credito': creditos_mes_actual,
            'debito': debitos_mes_actual,
            'otros': 0.0,  # Lógica adicional si es necesario
            'consumos': consumos_mes_actual,
            'saldo': saldo_actual,  # Saldo final (ajustado si es periodo anterior)
        })

    # Calcular el saldo inicial total y el total de consumos del mes
    saldo_inicial_total = sum(item['saldo_anterior'] for item in datos_tarjetas)
    total_consumos = sum(item['consumos'] for item in datos_tarjetas)

    # Preparar el contexto con los datos estructurados
    context = {
        'datos_tarjetas': datos_tarjetas,
        'periodo': periodo,
        'unidad': unidad,
        'saldo_inicial': saldo_inicial_total,
        'total_consumos': total_consumos,
    }
    
    return render(request, "costcenter/PeriodoAnterior/Totales_informacion.html", context)


def detalle_tarjeta_mes_actual(request, tarjeta):
    # Obtener mes y año actuales
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year

    # Obtener la tarjeta específica
    card = get_object_or_404(Cards, card_number=tarjeta, user=request.user)

    # Filtrar los consumos de la tarjeta en el mes y año actuales
    consumos = Consumo.objects.filter(
        card=card,
        consumo_date__month=mes_actual,
        consumo_date__year=anio_actual
    )

    # Calcular el total de consumos en el periodo actual
    total_consumo = consumos.aggregate(total=Sum('importe'))['total'] or 0.0

    # Calcular el saldo inicial de la tarjeta restando el total de consumos del saldo actual
    saldo_inicial = card.money - total_consumo

    # Manejo del formulario para agregar detalles
    if request.method == 'POST':
        form = ConsumoForm(request.POST)
        if form.is_valid():
            nuevo_consumo = form.save(commit=False)
            nuevo_consumo.card = card
            nuevo_consumo.consumo_date = datetime.now()  # Fecha actual para el nuevo consumo
            nuevo_consumo.save()
            return redirect('detalle_tarjeta_mes_actual', tarjeta=tarjeta)
    else:
        form = ConsumoForm()

    context = {
        'card': card,
        'saldo_inicial': saldo_inicial,
        'consumos': consumos,
        'total_consumo': total_consumo,
        'form': form,
    }
    return render(request, 'costcenter/PeriodoActual/detalle_tarjeta_mes.html', context)


def agregar_detalle(request, consumo_id):
    # Obtener el consumo específico por ID
    consumo = get_object_or_404(Consumo, consumo_id=consumo_id)
    card = consumo.card  # Obtener la tarjeta asociada al consumo

    if request.method == 'POST':
        # Actualizar los detalles del consumo desde el formulario
        consumo.tipo_de_gasto = request.POST.get('tipo_de_gasto') or None
        consumo.cantidad = request.POST.get('cantidad') or None
        consumo.un_med = request.POST.get('un_med') or None
        consumo.clase = request.POST.get('clase') or None
        consumo.monto_parcial = request.POST.get('monto_parcial') or None
        consumo.nro_factura = request.POST.get('numeroFactura') or None
        consumo.nro_movil = request.POST.get('numeroMovil') or None
        consumo.odometro = request.POST.get('odometro') or None

        # Guardar los detalles del consumo
        consumo.save()

        # Redireccionar de nuevo a la página de detalle de la tarjeta actual
        return redirect('detalle_tarjeta_mes_actual', tarjeta=consumo.card.card_number)
    print(consumo.num_ticket)
    # Pasar al contexto los datos de la tarjeta y el consumo, incluyendo los datos adicionales
    context = {
        'num_ticket': consumo.num_ticket or "",
        'consumo': consumo,
        'card_number': card.card_number,
        'card_name': card.card_name,
        'saldo_actual': card.money,
        'consumo_date': consumo.consumo_date,
        'importe': consumo.importe,
        'establecimiento': consumo.establecimiento,
        'numeroFactura': consumo.nro_factura or '',
        'numeroMovil': consumo.nro_movil or '',
        'odometro': consumo.odometro or '',
    }
    
    return render(request, 'costcenter/PeriodoActual/agregar_detalle.html', context)







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
