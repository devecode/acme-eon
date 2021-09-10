from django.contrib import admin
from .models import VentaProducto, VentaGeneral

admin.site.register(VentaGeneral)
admin.site.register(VentaProducto)
