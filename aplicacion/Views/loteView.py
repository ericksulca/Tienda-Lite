# -*- coding: utf-8 -*-
# Create your views here.
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from app import settings
from django.contrib.auth.decorators import login_required
from aplicacion.models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import json

class LoteList(ListView):
    model = Lote
    template_name = 'venta/listar.html'
    paginate_by = 10
    def get_queryset(self):
        new_context = Lote.objects.filter(
            estado=True,
        ).order_by('-fecha')
        return new_context

@csrf_exempt
def nuevoLote(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        productos = Datos["productos"]
        print(productos)
        oLote = Lote()
        oLote.save()
        #a1.publications.add(p1)
        for producto in productos:
            oProducto = Producto.objects.get(codigo = producto[1])
            cantidad = float(producto[0])
            oProducto.cantidad = oProducto.cantidad + cantidad
            oProducto.save()
            oLote.productos.add(oProducto)
            oLote.save()
            oLoteProductos = LoteProductos.objects.get(producto = oProducto,lote = oLote)
            oLoteProductos.cantidad = cantidad
            oLoteProductos.save()
        return HttpResponse(json.dumps({'exito':1,'id_Lote': oLote.id}), content_type="application/json")
    else:
        return render(request, 'lote/nuevo.html', {})
