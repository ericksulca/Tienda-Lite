# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from embutidos import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from app.formularios.cierrecajaForm import *
from app.formularios.aperturacajaForm import *
from django.db.models import Sum

@login_required
def registrarCierrecaja(request):
    if request.method == 'POST':
        Datos = request.POST
        form = CierrecajaForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            try:
                oAperturacaja = Aperturacaja.objects.get(id=Datos['idApertura'],activo=True)
                form.aperturacaja = oAperturacaja
                form.save()
                oAperturacaja.activo = False
                oAperturacaja.save()
                return render(request, 'caja/cierreRegistrado.html')
            except Exception as e:
                return render(request, 'caja/cierreNoRegistrado.html')
        else:
            return render(request, 'caja/cierre.html')
    else:
        oCajas = Caja.objects.filter(estado=True)
        try:
            oAperturacaja = Aperturacaja.objects.latest('id')
            if  oAperturacaja.activo==True:
                monto = Venta.objects.filter(estado=1,aperturacaja = oAperturacaja).aggregate(Sum('monto'))
                form = CierrecajaForm(initial={'monto':monto["monto__sum"]})
                return render(request, 'caja/cierre.html', {'form': form,'Aperturacaja': oAperturacaja,'monto': monto["monto__sum"],'cajas':oCajas})
            else:
                return render(request, 'caja/cierreNoRegistrado.html', {'cajas':oCajas})
        except Exception as e:
            #print e
            return render(request, 'caja/cierreNoRegistrado.html', {'cajas':oCajas})

@login_required
def registrarAperturacaja(request):
    if request.method == 'POST':
        Datos = request.POST
        form = AperturacajaForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            oCaja = Caja()
            oCaja.id = Datos['cmbCaja']
            form.caja = oCaja
            form.save()
            return render(request, 'caja/aperturaRegistrada.html')
        else:
            return render(request, 'caja/apertura.html')
    else:
        oCajas = Caja.objects.filter(estado=True)
        form = AperturacajaForm()
        try:
            oAperturacaja = Aperturacaja.objects.latest('id')
            if  oAperturacaja.activo==True:
                return render(request, 'caja/aperturaRegistrada.html', {'Aperturacaja': oAperturacaja})
            else:
                return render(request, 'caja/apertura.html', {'form': form,'cajas':oCajas})

        except Exception as e:
            return render(request, 'caja/apertura.html', {'form': form,'cajas':oCajas})

