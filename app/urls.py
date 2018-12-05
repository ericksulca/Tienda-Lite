"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from aplicacion.views import *
from aplicacion.Views.ventaView import *
from aplicacion.Views.loteView import *
from aplicacion.Views.productoView import *
from aplicacion.Views.cajaView import *
from aplicacion.Views.reporteView import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', nuevaVenta),
    url(r'^login/$', Login),
    url(r'^logout/$', Logout),
    url(r'^home/$', nuevaVenta),
    ################## VENTA ##############################
    url(r'^venta/$', nuevaVenta),
    url(r'^venta/nuevo/$', nuevaVenta),
    url(r'^venta/detalle/(?P<id_venta>\d+)/$', nuevaVenta),
    url(r'^venta/insertar/$', insertarVenta),
    url(r'^venta/imprimir/$', imprimirVenta),
    url(r'^venta/anular/(?P<id_venta>\d+)/$$', anularVenta),
    url(r'^venta/imprimir/(?P<id_venta>\d+)/$', imprimirVentaGET),
    url(r'^venta/listar', login_required(VentaList.as_view()), name='mascota_listar'),

    ################## PRODUCTO ########################
    url(r'^producto/nuevo/$', nuevoProducto),
    url(r'^producto/detalle/$', nuevoProducto),
    url(r'^producto/editar/$', nuevoProducto),
    #url(r'^producto/listar/$', listarProducto),
    url(r'^producto/buscar/$', BuscarProducto),
    url(r'^producto/listar', login_required(ProductoList.as_view()), name='producto_listar'),
    url(r'^producto/editar/(?P<pk>\d+)/$', login_required(ProductoUpdate.as_view()), name='producto_editar'),
    ################## REPORTES ###########################(?P<pk>\d+)/
    url(r'^reporte/venta/$', reporteVenta),
    url(r'^reporte/caja/$', reporteCierreCaja),
    url(r'^reporte/venta/$', reporteVenta),
    ################## LOTE ###########################(?P<pk>\d+)/

    url(r'^lote/listar/$', login_required(LoteList.as_view()), name='producto_listar'),
    url(r'^lote/nuevo/$', nuevoLote),

    ################## CAJA ###############################
    url(r'^caja/apertura/$', registrarAperturacaja),
    url(r'^caja/cierre/$', registrarCierrecaja),
    #url(r'^Caja/movimiento/$', registrarOperacion),
]