from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from aplicacion.models import *

class AperturacajaForm(ModelForm):
    class Meta:
        model = Aperturacaja
        fields = ('monto',)
