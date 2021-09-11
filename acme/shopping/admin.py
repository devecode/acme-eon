from django.contrib import admin
from .models import CompraProducto, CompraGeneral


class CompraGeneralAdmin(admin.ModelAdmin):
    list_display = ['pk', 'fc', 'usuario', 'articulo_total', 'total','total_efectivo','total_tarjeta', 'metodo_pago']

class CompraProductoAdmin(admin.ModelAdmin):
    list_display = ['pk','num_venta','cantidad','producto' ,'venta',
                        'importe'
                    ]



admin.site.register(CompraProducto, CompraProductoAdmin)
admin.site.register(CompraGeneral, CompraGeneralAdmin)
