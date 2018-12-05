# -*- coding: utf-8 -*-
# Create your views here.
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from embutidos import settings
from django.contrib.auth.decorators import login_required
from app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import json

class VentaList(ListView):
    model = Venta
    template_name = 'venta/listar.html'
    paginate_by = 50

@login_required
def anularVenta(request):
    if request.method == 'POST':
        Datos = request.POST
        if Datos["NroVenta"]:
            idVenta = Datos["NroVenta"]
            oVenta = Venta.objects.get(id= idVenta,estado=True)
            oVentaproductos = Ventaproductos.objects.filter(venta = oVenta,estado=True)
            return render(request, 'venta/anular.html', {'oVenta':oVenta,'oVentaproductos':oVentaproductos})
        if Datos["id_venta"]:
            return render(request, 'venta/anular.html', {'oVenta':oVenta})
    if request.method == 'GET':
        return render(request, 'venta/buscar.html', {})

@login_required
def nuevaVenta(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")
    else:
        # revisar el estado de la caja Abierto o Cerrado!!!!!!!!
        oAperturacaja = Aperturacaja.objects.latest('id')
        if  oAperturacaja.activo==False:
            return render(request, 'caja/aperturaNoRegistrada.html', {'Aperturacaja': oAperturacaja})
        else:
            return render(request, 'venta/nuevo.html', {})



#@login_required
@csrf_exempt
def imprimirVenta(request):
    if request.method == 'POST':
        Datos = request.POST
        idVenta = Datos["NroVenta"]
        try:
            oVenta = Venta.objects.get(id = idVenta)
            cliente = ""
            direccion = ""
            fecha = str(oVenta.fecha)
            documento = ""
            oVentaproductos = Ventaproductos.objects.filter(estado = True,venta = oVenta)
            return render(request, 'venta/reciboBoleta.html', {'oVentaproductos': oVentaproductos,'total_venta':oVenta.monto,'cliente':cliente,'direccion':direccion,'fecha':fecha,'documento':documento})
        except Exception as e:
            return render(request, 'venta/reciboBoleta.html', {})
    if request.method == 'GET':
        return render(request, 'venta/buscar.html', {})

@csrf_exempt
def imprimirVentaGET(request,id_venta):
    if request.method == 'GET':
        idVenta = id_venta
        try:
            oVenta = Venta.objects.get(id = idVenta)
            cliente = " "
            direccion = " "
            fecha = str(oVenta.fecha)
            documento = " "
            oVentaproductos = Ventaproductos.objects.filter(estado = True,venta = oVenta)
            return render(request, 'venta/reciboBoleta.html', {'oVentaproductos': oVentaproductos,'total_venta':oVenta.monto,'cliente':cliente,'direccion':direccion,'fecha':fecha,'documento':documento})
        except Exception as e:
            return render(request, 'venta/reciboBoleta.html', {})
    if request.method == 'GET':
        return render(request, 'venta/buscar.html', {})

@csrf_exempt
def insertarVenta(request):
     if request.method == 'POST':
        Datos = json.loads(request.body)
        productos = Datos["productos"]
        #print productos
        oVenta = Venta()
        oAperturacaja = Aperturacaja.objects.latest('id')
        oVenta.aperturacaja = oAperturacaja
        oVenta.save()
        Total = 0
        for producto in productos:
            monto = 0
            oProducto = Producto.objects.filter(codigo = producto[1])
            oProducto = oProducto[0]
            oVentaproductos = Ventaproductos()
            cantidad = float(producto[0])
            oVentaproductos.producto = oProducto
            oVentaproductos.venta = oVenta
            oVentaproductos.cantidad = cantidad
            oVentaproductos.precioventa = producto[2]
            oVentaproductos.save()
            cantidadAnterior = oProducto.cantidad 
            oProducto.cantidad = cantidadAnterior - cantidad
            oProducto.save()
            monto = float(producto[2])
            Total = Total + monto
        oVenta.monto = Total
        oVenta.save()
        return HttpResponse(json.dumps({'exito':1,'id_venta': oVenta.id}), content_type="application/json")