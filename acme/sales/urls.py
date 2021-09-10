from django.urls import path
from .views import VentaGeneralList, nombreProductoSearch, apliacionVenta, VentaG
 

urlpatterns = [
    path('ventas-generales',VentaG.as_view(), name='ventas_generales'),

    path('ventas',VentaGeneralList.as_view(), name='ventas'),
    path('producto/<str:bar_id>/',nombreProductoSearch, name='busqueda'),
    path('aplicacionVenta',apliacionVenta, name='venta'),
]