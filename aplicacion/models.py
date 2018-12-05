from __future__ import unicode_literals

from django.db import models


class Caja(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField(blank=True,default=True)

class Aperturacaja(models.Model):
    fecha  = models.DateTimeField(auto_now_add=True, blank=True)
    monto  = models.FloatField()
    activo = models.BooleanField(blank=True,default=True)
    estado = models.BooleanField(blank=True,default=True)
    caja   = models.ForeignKey('Caja',on_delete=models.CASCADE)  # Field name made lowercase.

class Cierrecaja(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, blank=True)
    monto = models.FloatField()
    estado = models.BooleanField(blank=True,default=True)
    aperturacaja = models.ForeignKey(Aperturacaja,on_delete=models.CASCADE)  # Field name made lowercase.

class Producto(models.Model):
    nombre       = models.CharField(max_length=45)
    codigo       = models.CharField(max_length=45, blank=True, null=True)
    unidad       = models.CharField(max_length=10, blank=True, null=True)
    cantidad     = models.FloatField(default=0,blank=True, null=True)
    imagen       = models.ImageField(blank=True, null=True)#upload_to='%Y/%m/%d',
    url          = models.CharField(max_length=100, blank=True, null=True)
    precioxmenor = models.FloatField(blank=True)
    precioxmayor = models.FloatField(blank=True, null=True)
    estado       = models.BooleanField(blank=True,default=True)

    class Meta:
        ordering = ["nombre"]
    def __str__(self):
        return self.nombre

class Lote(models.Model):
    fecha      = models.DateTimeField(auto_now_add=True, blank=True)
    modificado = models.DateTimeField(auto_now=True, blank=True)
    proveedor  = models.CharField(max_length=45)  # Field name made lowercase.
    productos  = models.ManyToManyField(Producto)
    estado     = models.BooleanField(blank=True,default=True)

from django.contrib.auth.models import User
class Anulacionventa(models.Model):
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    descripcion  = models.TextField(blank=True,null=True)
    usuario      = models.ForeignKey(User,on_delete=models.CASCADE)
    estado       = models.BooleanField(blank=True,default=True)

class Venta(models.Model):
    fecha          = models.DateTimeField(auto_now_add=True, blank=True)
    monto          = models.FloatField(blank=True, null=True)
    nrecibo        = models.CharField(max_length=45, blank=True, null=True)
    productos      = models.ManyToManyField(Producto)
    aperturacaja   = models.ForeignKey(Aperturacaja,on_delete=models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    anulacionventa = models.ForeignKey(Anulacionventa,on_delete=models.CASCADE, blank=True, null=True, default = '')
    estado         = models.BooleanField(blank=True,default=True)

    class Meta:
        ordering = ["-fecha"]
    def __str__(self):
        cadena = str(self.fecha)+" - "+str(self.monto)
        return cadena

class Ventaproductos(models.Model):
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    modificacion = models.DateTimeField(auto_now=True, blank=True)
    cantidad     = models.FloatField(default=0,blank=True, null=True)
    precioventa  = models.FloatField(default=0,blank=True, null=True)
    venta        = models.ForeignKey(Venta,on_delete=models.CASCADE)
    producto     = models.ForeignKey(Producto,on_delete=models.CASCADE)
    activo       = models.BooleanField(blank=True,default=True)
    estado       = models.BooleanField(blank=True,default=True)

    class Meta:
        managed = False
        db_table = 'aplicacion_venta_productos'

class LoteProductos(models.Model):
    fecha        = models.DateTimeField(auto_now_add=True, blank=True)
    modificacion = models.DateTimeField(auto_now=True, blank=True)
    cantidad     = models.FloatField(default=0,blank=True, null=True)
    lote        = models.ForeignKey(Lote,on_delete=models.CASCADE)
    producto     = models.ForeignKey(Producto,on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'aplicacion_lote_productos'