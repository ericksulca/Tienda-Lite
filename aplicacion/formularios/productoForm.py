from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from aplicacion.models import *

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre','codigo','cantidad','imagen','precioxmenor','precioxmayor',)
