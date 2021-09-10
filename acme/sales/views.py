from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import requires_csrf_token
import json
from django.core import serializers
from django.contrib.auth.models import User
import io
from django.http import FileResponse
from .models import VentaGeneral, VentaProducto
from users.models import Profile
from products import models as modelsInv




class VentaG(LoginRequiredMixin, generic.ListView):
    login_url = "users:login"
    model = VentaGeneral
    permission_required='sales.view_ventageneral'
    template_name = 'sales/ventageneral_list.html'
    context_object_name = 'obj'


class VentaGeneralList(LoginRequiredMixin, generic.ListView):
    login_url = "users:login"
    model = VentaGeneral
    permission_required='sales.view_ventageneral'
    template_name = 'sales/venta_new.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = modelsInv.Product.objects.all
        context['productos'] = productos
        return context


def nombreProductoSearch(request, bar_id):
    response = modelsInv.Product.objects.filter(nombre=bar_id)
    if response:
        data = serializers.serialize('json', response)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponseBadRequest()

@requires_csrf_token
def apliacionVenta(request):
    if request.method == 'POST':
        post = json.loads(request.body)
        try:
            import datetime
            now = datetime.datetime.now()
            user = User.objects.get(username=post["user"])
            metodo = ''
            if float(post["efectivo"]) != 0 and float(post["tarjeta"]) != 0:
                metodo = 'MIXTO'
            elif (float(post["efectivo"]) == 0):
                metodo = 'TARJETA'
            else:
                metodo = 'EFECTIVO'

            venta = VentaGeneral(metodo_pago=metodo,usuario=user, total_efectivo=float(post["efectivo"]), total_tarjeta=float(post["tarjeta"]))

            venta.save()
            
        except:
            #Error, ocurrió un problema
            return HttpResponse("400", content_type="text/plain")

        try:
            for product in post["productos"]:
                #print(product["producto"])
                prod = modelsInv.Product.objects.get(nombre=product["producto"])
                ventaProd = VentaProducto(cantidad=float(product["cantidad"]), producto=prod, num_venta=venta)
                ventaProd.save()
        except :
            #Para borra el registro si algo sale mal
            VentaGeneral.objects.filter(id=venta.pk).delete()

            #Error, ocurrió un problema
            return HttpResponseBadRequest()
            #return HttpResponse("400", content_type="text/plain")

        #Venta correctamente registrada
        return HttpResponse(venta.pk, content_type="text/plain")
    else:
        return HttpResponseBadRequest()
