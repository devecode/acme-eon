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

class CompraGeneral(models.Model):
    METODO = [
        ('EFECTIVO', 'EFECTIVO'),
        ('TARJETA', 'TARJETA'),
        ('MIXTO', 'MIXTO'),
    ]
    articulo_total = models.BigIntegerField(default=0, editable=False)
    metodo_pago = models.CharField('METODO', choices=METODO, default='EFECTIVO', max_length=100, blank=True)
    fc = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=50, decimal_places=2,default=0, editable=False)
    total_efectivo = models.FloatField(default=0, editable=False)
    total_tarjeta = models.FloatField(default=0, editable=False)



    def __str__(self):
        return '{}'.format(self.pk)

    
class CompraProducto(models.Model):
    cantidad = models.IntegerField(default=0)
    producto = models.ForeignKey(Product, related_name='productos_nombre',  on_delete=models.CASCADE)
    venta = models.FloatField(default=0, editable=False)
    importe = models.FloatField(default=0, editable=False)
    usuario = models.ForeignKey(Profile, on_delete=models.CASCADE)
    num_venta = models.ForeignKey(CompraGeneral, on_delete=models.CASCADE)


    def __str__(self):
        return '{}'.format(self.pk)
    
    def save(self):
        self.venta = self.producto.precio
        self.importe = self.cantidad * self.venta
        super(CompraProducto,self).save()

@receiver(post_save, sender=CompraProducto)
def detalle_fac_guardar(sender,instance,**kwargs):
    num_venta_id = instance.num_venta.id
    producto_id = instance.producto.id
    usuario_id = instance.usuario.id

    vg = CompraGeneral.objects.get(pk=num_venta_id)
    if vg:
        cantidad = CompraProducto.objects\
            .filter(num_venta=num_venta_id) \
            .aggregate(cantidad=Sum('cantidad')) \
            .get('cantidad',0.00)
        importe = CompraProducto.objects\
            .filter(num_venta=num_venta_id) \
            .aggregate(importe=Sum('importe')) \
            .get('importe',0.00)
        

        
        vg.total = importe
        vg.articulo_total = cantidad 
        vg.save()

    prod=Product.objects.filter(pk=producto_id).first()
    
    if prod:
        cantidad = int(prod.stock_inicial) + int(instance.cantidad)
        prod.stock_inicial = cantidad
        prod.stock_final = cantidad
        prod.save()
    
    usuario=Profile.objects.filter(pk=usuario_id).first()
    
    if usuario:
        importe = int(usuario.saldo_inicial) - int(instance.importe)
        usuario.saldo_inicial = importe
        usuario.saldo_final = importe
        usuario.save()
