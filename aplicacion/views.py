# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from app import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from aplicacion.models import *
from django.views.decorators.csrf import csrf_exempt
import json

def Login(request):
    next = request.GET.get('next', '/home/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        #print user
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, "login/login.html", {'redirect_to': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

@login_required
def Home(request):
    return render(request, "inicio/index.html", {'redirect_to': next})

def Prueba(request):
    oCaja = Caja.objects.filter(estado=1)
    #print oCaja
    return HttpResponse(json.dumps({'exito':1}), content_type="application/json")


@login_required
def descontarVenta(request):
    if request.method == 'GET':
        oVentas = Venta.objects.filter(estado=True)
        for oVenta in oVentas:
            for oProductoVenta in oVenta.productos.filter(estado=True):
                #print (oProductoVenta.id)
                #print (oProductoVenta.cantidad)
                try:
                    oProducto = Producto.objects.get(id= oProductoVenta.id)
                    oVentaproductos = Ventaproductos.objects.get(producto = oProducto, venta = oVenta)
                    oProducto.cantidad=oProducto.cantidad - oVentaproductos.cantidad
                    oProducto.save()
                    print ("Correcto")
                except:
                    print ("error en producto.id: ")
                    print (oProductoVenta.id)
        return HttpResponse("Listo!")

@login_required
def ingresarLote(request):
    if request.method == 'GET':
        oLotes = Lote.objects.filter(estado=True)
        for oLote in oLotes:
            for oProductoLote in oLote.productos.filter(estado=True):
                #print (oProductoLote.id)
                try:
                    oProducto = Producto.objects.get(id= oProductoLote.id)
                    oLoteProducto = LoteProductos.objects.get(lote=oLote,producto = oProducto)
                    oProducto.cantidad=oProducto.cantidad + oLoteProducto.cantidad
                    oProducto.save()
                    #print (oProductoLote.id)
                    #print ("Correcto")
                    print (oProducto.cantidad)
                except:
                    print ("error en producto.id: ")
                    print (oProductoVenta.id)
        return HttpResponse("Listo!")