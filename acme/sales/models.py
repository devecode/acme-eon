from django.db import models
from django.contrib.auth.models import User
#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Sum
#Models Producto
from products.models import Product
#Models Profile
from users.models import Profile

class VentaGeneral(models.Model):
    METODO = [
        ('EFECTIVO', 'EFECTIVO'),
        ('TARJETA', 'TARJETA'),
        ('MIXTO', 'MIXTO'),
    ]
    articulo_total = models.BigIntegerField(default=0, editable=False)
    metodo_pago = models.CharField('METODO', choices=METODO, default='EFECTIVO', max_length=100, blank=True)
    fc = models.DateTimeField(auto_now_add=True)
    #hc = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=50, decimal_places=2,default=0, editable=False)
    total_efectivo = models.FloatField(default=0, editable=False)
    total_tarjeta = models.FloatField(default=0, editable=False)


    #objects = VentaGeneralManager()

    def __str__(self):
        return '{}'.format(self.pk)

    
class VentaProducto(models.Model):
    cantidad = models.IntegerField(default=0)
    producto = models.ForeignKey(Product, related_name='producto_nombre',  on_delete=models.CASCADE)
    venta = models.FloatField(default=0, editable=False)
    importe = models.FloatField(default=0, editable=False)
    usuario = models.ForeignKey(Profile, on_delete=models.CASCADE)
    num_venta = models.ForeignKey(VentaGeneral, on_delete=models.CASCADE)


    def __str__(self):
        return '{}'.format(self.pk)
    
    def save(self):
        self.venta = self.producto.precio
        self.importe = self.cantidad * self.venta
        super(VentaProducto,self).save()

@receiver(post_save, sender=VentaProducto)
def detalle_fac_guardar(sender,instance,**kwargs):
    num_venta_id = instance.num_venta.id
    producto_id = instance.producto.id
    usuario_id = instance.usuario.id

    vg = VentaGeneral.objects.get(pk=num_venta_id)
    if vg:
        cantidad = VentaProducto.objects\
            .filter(num_venta=num_venta_id) \
            .aggregate(cantidad=Sum('cantidad')) \
            .get('cantidad',0.00)
        importe = VentaProducto.objects\
            .filter(num_venta=num_venta_id) \
            .aggregate(importe=Sum('importe')) \
            .get('importe',0.00)
        

        
        vg.total = importe
        vg.articulo_total = cantidad 
        vg.save()

    prod=Product.objects.filter(pk=producto_id).first()
    
    if prod:
        cantidad = int(prod.stock_inicial) - int(instance.cantidad)
        prod.stock_inicial = cantidad
        prod.stock_final = cantidad
        prod.save()
    
    saldo=Profile.objects.filter(pk=usuario_id).first()
    
    if saldo:
        importe = float(saldo.saldo_inicial) - int(instance.importe)
        saldo.saldo_inicial = importe
        saldo.saldo_final = importe
        saldo.save()
