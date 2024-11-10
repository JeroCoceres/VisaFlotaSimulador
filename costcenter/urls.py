from django.urls import path

from django_base.views import index
from costcenter.views import create_transaction,test,InformacionPorCentroDeCostosActual,InformacionYMovimientosPorTarjetasActual,InformacionPorCentroDeCostosAnterior,InformacionYMovimientosPorTarjetasAnterior,InformacionYMovimientosPorTarjetasAnterior, RealizarDistribucionPorOrdenAlfabetico, RealizarDistribucion
from costcenter.views import DistribucionesDeFondosRealizadas, RealizarTransferenciasPorOrdenAlfabetico, RealizarTransferencias, TransferenciasRealizadas, RealizarDevoluciones, DevolucionesRealizadas
from costcenter.views import AutorizacionesPorTarjetas, RendicionesPorCentroDeCostosPDF, RendicionesPorCentroDeCostosXLSX, RendicionPorCuentaPDF, RendicionPorCuentaXLSX, MovimientosPorTarjetasPDF, MovimientosPorTarjetasXLSX, UltimasLiquidaciones
from costcenter.views import show_cards, get_user_cards_destiny, get_user_cards_origen,InformacionPorCentroDeCostosAnterior_Totales, transaction_success

urlpatterns = [
    path('transaction/new/', create_transaction, name='create_transaction'),
    path("test/",test),
    path('cards/', show_cards, name='show_cards'),
    path('get_user_cards_origen/', get_user_cards_origen, name='get_user_cards_origen'),
    path('get_user_cards_destiny/', get_user_cards_destiny, name='get_user_cards_destiny'),

    path("infoPorCentroDeCostosActual/",InformacionPorCentroDeCostosActual),
    path("InformacionYMovimientosPorTarjetasActual/",InformacionYMovimientosPorTarjetasActual),

    path("InformacionPorCentroDeCostosAnterior/",InformacionPorCentroDeCostosAnterior,name='informacion_por_centro_anterior'),
    path("InformacionPorCentroDeCostosAnterior/TotalesPorCentroDeCostos/<str:periodo>/", InformacionPorCentroDeCostosAnterior_Totales, name='totales_informacion'),


    path("InformacionYMovimientosPorTarjetasAnterior/",InformacionYMovimientosPorTarjetasAnterior),
    path("AutorizacionesPorTarjetas/",AutorizacionesPorTarjetas),
    path("RealizarDistribucionPorOrdenAlfabetico/",RealizarDistribucionPorOrdenAlfabetico),


    path("RealizarDistribucion/",RealizarDistribucion, name='realizar_distribucion'),


    path("DistribucionesDeFondosRealizadas/",DistribucionesDeFondosRealizadas),
    path("RealizarTransferenciasPorOrdenAlfabetico/",RealizarTransferenciasPorOrdenAlfabetico),
    
    path("RealizarTransferencias/",RealizarTransferencias),
    path('transaction_success/', transaction_success, name='transaction_success'),


    path("TransferenciasRealizadas/",TransferenciasRealizadas),
    path("RealizarDevoluciones/",RealizarDevoluciones),
    path("DevolucionesRealizadas/",DevolucionesRealizadas),
    path("RendicionesPorCentroDeCostosPDF/",RendicionesPorCentroDeCostosPDF),
    path("RendicionesPorCentroDeCostosXLSX/",RendicionesPorCentroDeCostosXLSX),
    path("RendicionPorCuentaPDF/",RendicionPorCuentaPDF),
    path("RendicionPorCuentaXLSX/",RendicionPorCuentaXLSX),
    path("MovimientosPorTarjetasPDF/",MovimientosPorTarjetasPDF),
    path("MovimientosPorTarjetasXLSX/",MovimientosPorTarjetasXLSX),
    path("UltimasLiquidaciones/",UltimasLiquidaciones),
]

