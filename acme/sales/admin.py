from django.contrib import admin
from .models import VentaProducto, VentaGeneral


class VentaGeneralAdmin(admin.ModelAdmin):
    list_display = ['pk', 'fc', 'usuario', 'articulo_total', 'total','total_efectivo','total_tarjeta', 'metodo_pago']

class VentaProductoAdmin(admin.ModelAdmin):
    list_display = ['pk','num_venta','cantidad','producto' ,'venta',
                        'importe'
                    ]



admin.site.register(VentaProducto, VentaProductoAdmin)
admin.site.register(VentaGeneral, VentaGeneralAdmin)
