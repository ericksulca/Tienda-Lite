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

@login_required
def reporteVenta(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")
    else:
        return render(request, 'reportes/reporteVenta.html', {})

@login_required
def reporteCierreCaja(request):
    if request.method == 'POST':
        Datos = json.loads(request.body)
        return HttpResponse(json.dumps({'exito':1}), content_type="application/json")
    else:
        return render(request, 'reportes/reporteVenta.html', {})