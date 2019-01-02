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
from aplicacion.formularios.productoForm import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

class UserListView(ListView):
    model = User
    template_name = 'core/user_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'users'  # Default: object_list
    paginate_by = 10
    queryset = User.objects.all()  # Default: Model.objects.all()

class ProductoList(ListView):
    model = Producto
    #print model
    template_name = 'producto/listar.html'
    paginate_by = 30
    queryset = Producto.objects.filter(estado=True)  # Default: Model.objects.all()

class ProductoUpdate(UpdateView):
    model = Producto
    fields = ['name']
    template_name_ = 'producto/editar.html'


@login_required
def listarProducto(request):
    if request.method == 'POST':
        # MODIFICAR PARA EL FILTRO DE PRODUCTOS
        oProductos = Producto.objects.filter(estado=True)
        return render(request,'producto/listar.html',{'oProductos':oProductos})
    if request.method == 'GET':
        oProductos = Producto.objects.filter(estado=True).order_by('nombre')
        return render(request,'producto/listar.html',{'oProductos':oProductos})

@login_required
def nuevoProducto(request):
    if request.method == 'POST':
        Datos = request.POST
        form = ProductoForm(request.POST)
        if form.is_valid():
            try:
                form = form.save()
                return HttpResponseRedirect('/producto/listar/')
            except Exception as e:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        form = ProductoForm()
        return render(request, 'producto/registrar.html', {'form': form})

@csrf_exempt
def BuscarProducto (request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        nombreProducto = Datos["nombreProducto"]
        oProductos = []
        oProductosNombre = Producto.objects.filter(nombre__icontains=nombreProducto,estado = True)
        if oProductosNombre.count() != 0:
            oProductos = oProductosNombre
        oProductosCodigo = Producto.objects.filter(codigo__icontains=nombreProducto,estado = True)
        if oProductosCodigo.count() != 0:
            oProductos.append(oProductosCodigo[0])
        jsonProductos = {}
        jsonProductos["productos"] = []
        for oProducto in oProductos:
            jsonProducto = {}
            jsonProducto["id"] = oProducto.id
            jsonProducto["nombre"] = oProducto.nombre
            jsonProducto["codigo"] = oProducto.codigo
            jsonProducto["precio"] = oProducto.precioxmenor
            jsonProductos["productos"].append(jsonProducto)

        return HttpResponse(json.dumps(jsonProductos), content_type="application/json")