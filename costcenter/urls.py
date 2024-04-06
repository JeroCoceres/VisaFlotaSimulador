from django.urls import path

from django_base.views import index
from costcenter.views import create_transaction,test,InformacionPorCentroDeCostosActual,InformacionYMovimientosPorTarjetasActual,InformacionPorCentroDeCostosAnterior,InformacionYMovimientosPorTarjetasAnterior,InformacionYMovimientosPorTarjetasAnterior, RealizarDistribucionPorOrdenAlfabetico, RealizarDistribucion
from costcenter.views import DistribucionesDeFondosRealizadas, RealizarTransferenciasPorOrdenAlfabetico, RealizarTransferencias, TransferenciasRealizadas, RealizarDevoluciones, DevolucionesRealizadas
from costcenter.views import AutorizacionesPorTarjetas, RendicionesPorCentroDeCostosPDF, RendicionesPorCentroDeCostosXLSX, RendicionPorCuentaPDF, RendicionPorCuentaXLSX, MovimientosPorTarjetasPDF, MovimientosPorTarjetasXLSX, UltimasLiquidaciones


urlpatterns = [
    path("new_transaction/", create_transaction, name="create_transaction"),
    path("test/",test),
    path("InformacionPorCentroDeCostosActual/",InformacionPorCentroDeCostosActual),
    path("InformacionYMovimientosPorTarjetasActual/",InformacionYMovimientosPorTarjetasActual),
    path("InformacionPorCentroDeCostosAnterior/",InformacionPorCentroDeCostosAnterior),
    path("InformacionYMovimientosPorTarjetasAnterior/",InformacionYMovimientosPorTarjetasAnterior),
    path("AutorizacionesPorTarjetas/",AutorizacionesPorTarjetas),
    path("RealizarDistribucionPorOrdenAlfabetico/",RealizarDistribucionPorOrdenAlfabetico),
    path("RealizarDistribucion/",RealizarDistribucion),
    path("DistribucionesDeFondosRealizadas/",DistribucionesDeFondosRealizadas),
    path("RealizarTransferenciasPorOrdenAlfabetico/",RealizarTransferenciasPorOrdenAlfabetico),
    path("RealizarTransferencias/",RealizarTransferencias),
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

