from django.urls import path

from django_base.views import index
from costcenter.views import create_transaction,test,InformacionPorCentroDeCostosActual,InformacionYMovimientosPorTarjetasActual,InformacionPorCentroDeCostosAnterior,InformacionYMovimientosPorTarjetasAnterior,InformacionYMovimientosPorTarjetasAnterior, RealizarDistribucion
from costcenter.views import DistribucionesDeFondosRealizadas, RealizarTransferencias, TransferenciasRealizadas, RealizarDevoluciones, DevolucionesRealizadas
from costcenter.views import AutorizacionesPorTarjetas, RendicionPorCuentaPDF, RendicionPorCuentaXLSX, MovimientosPorTarjetasPDF, MovimientosPorTarjetasXLSX, UltimasLiquidaciones
from costcenter.views import show_cards, get_user_cards_destiny, get_user_cards_origen,InformacionPorCentroDeCostosAnterior_Totales, transaction_success, detalle_tarjeta_mes, totales_informacion_actual,detalle_tarjeta_mes_actual,agregar_detalle
from costcenter.views import consulta_distribuciones, detalle_distribucion, generar_xls_rendicion_cc, admin_panel
from costcenter.views import consulta_transferencias, detalle_transferencia, TransferenciasDeFondosRealizadas, generar_pdf_rendicion_cc


from costcenter.views import admin_manage_cards

urlpatterns = [
    path('transaction/new/', create_transaction, name='create_transaction'),
    path("test/",test),
    path('cards/', show_cards, name='show_cards'),
    path('get_user_cards_origen/', get_user_cards_origen, name='get_user_cards_origen'),
    path('get_user_cards_destiny/', get_user_cards_destiny, name='get_user_cards_destiny'),

    path("InformacionPorCentroDeCostosActual/",InformacionPorCentroDeCostosActual,name='InformacionPorCentroDeCostosActual'),
    path("InformacionYMovimientosPorTarjetasActual/",InformacionYMovimientosPorTarjetasActual),
    path('costcenter/totales_informacion_actual/', totales_informacion_actual, name='totales_informacion_actual'),
    path('costcenter/detalle_tarjeta_mes_actual/<int:tarjeta>/', detalle_tarjeta_mes_actual, name='detalle_tarjeta_mes_actual'),
    path('agregar_detalle/<int:consumo_id>/', agregar_detalle, name='agregar_detalle'),


    path("InformacionPorCentroDeCostosAnterior/",InformacionPorCentroDeCostosAnterior,name='informacion_por_centro_anterior'),
    path("InformacionPorCentroDeCostosAnterior/TotalesPorCentroDeCostos/<str:periodo>/", InformacionPorCentroDeCostosAnterior_Totales, name='totales_informacion'),
    path("detalle_tarjeta/<int:tarjeta>/<str:periodo>/",detalle_tarjeta_mes, name='detalle_tarjeta_mes'),



    path('InformacionYMovimientosPorTarjetasAnterior/', InformacionYMovimientosPorTarjetasAnterior, name='InformacionYMovimientosPorTarjetasAnterior'),


    path("AutorizacionesPorTarjetas/",AutorizacionesPorTarjetas),
    path('distribucion/<int:distribucion_id>/', detalle_distribucion, name='detalle_distribucion'),



    path("RealizarDistribucion/",RealizarDistribucion, name='realizar_distribucion'),
    path('distribuciones/consulta/', consulta_distribuciones, name='consulta_distribuciones'),
    path('distribuciones/detalle/<int:distribucion_id>/', detalle_distribucion, name='detalle_distribucion'),



    path("DistribucionesDeFondosRealizadas/",DistribucionesDeFondosRealizadas),
    
    path("RealizarTransferencias/",RealizarTransferencias),
    path('transaction_success/', transaction_success, name='transaction_success'),
    path('transferencias/consulta/', consulta_transferencias, name='consulta_transferencias'),
    path('transferencias/detalle/<int:transferencia_id>/', detalle_transferencia, name='detalle_transferencia'),
    path("TransferenciasDeFondosRealizadas/", TransferenciasDeFondosRealizadas, name='transferencias_realizadas'),


    path('RendicionesPorCentroDeCostosPDF/', generar_pdf_rendicion_cc, name='generar_pdf_rendicion_cc'),
    path('costcenter/RendicionesPorCentroDeCostosPDF/', generar_pdf_rendicion_cc, name='rendiciones_pdf'),
    path('costcenter/RendicionesPorCentroDeCostosXLS/', generar_xls_rendicion_cc, name='generar_xls_rendicion_cc'),

    path("MovimientosPorTarjetasPDF/",MovimientosPorTarjetasPDF, name='mov_tarjeta_pdf'),
    path("MovimientosPorTarjetasXLSX/",MovimientosPorTarjetasXLSX, name='mov_tarjeta_xls'),

    path("RendicionPorCuentaPDF/",RendicionPorCuentaPDF, name="rendicion_cuenta_pdf"),
    path("RendicionPorCuentaXLSX/",RendicionPorCuentaXLSX, name="rendicion_cuenta_xls"),

    path("TransferenciasRealizadas/",TransferenciasRealizadas),
    path("RealizarDevoluciones/",RealizarDevoluciones),
    path("DevolucionesRealizadas/",DevolucionesRealizadas),
    path("UltimasLiquidaciones/",UltimasLiquidaciones),

    path('admin_panel/',admin_panel, name='admin_panel'),

    path("admin/cards/manage/", admin_manage_cards, name="admin_manage_cards"),
]

