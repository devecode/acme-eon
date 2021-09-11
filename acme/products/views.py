from django.shortcuts import HttpResponseRedirect, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from .models import Categorie, Product
from .forms import *


class CategoriaList(LoginRequiredMixin, generic.ListView):
    #login_url = "contabilidad:login"
    model = Categorie
    permission_required='products.view_categorie'
    template_name = 'products/categoria_list.html'
    context_object_name = 'obj'

class CategoriaNew(LoginRequiredMixin, SuccessMessageMixin,\
    generic.CreateView):
    login_url = "contabilidad:login"
    permission_required="products.add_categorie"
    model=Categorie
    template_name="products/categoria_form.html"
    context_object_name = "obj"
    form_class=CategoriaForm
    success_url=reverse_lazy("products:categoria")
    success_message="Categoria Creada Satisfactoriamente"

class CategoriaEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Categorie
    template_name = "products/categoria_form.html"
    context_object_name = 'obj'
    form_class = CategoriaForm
    success_url = reverse_lazy("products:categoria")
    success_message = "Categoría Editada Correctamente"
    permission_required = "products.change_categorie"

class CategoriaDel(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    permission_required = "componentes.delete_categorie"
    model = Categorie
    template_name = "products/del.html"
    context_object_name = "obj"
    success_url= reverse_lazy("products:categoria")
    success_message="Categoría borrada satisfactoriamente"


class ProductoList(LoginRequiredMixin, generic.ListView):
    #login_url = "contabilidad:login"
    model = Product
    permission_required='products.view_product'
    template_name = 'products/producto_list.html'
    context_object_name = 'obj'

class ProductoNew(LoginRequiredMixin, SuccessMessageMixin,\
    generic.CreateView):
    login_url = "contabilidad:login"
    permission_required="products.add_product"
    model=Product
    template_name="products/producto_form.html"
    context_object_name = "obj"
    form_class=ProductoForm
    success_url=reverse_lazy("products:producto")
    success_message="Producto Creado Satisfactoriamente"

class ProductoEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Product
    template_name = "products/producto_form.html"
    context_object_name = 'obj'
    form_class = ProductoForm
    success_url = reverse_lazy("products:producto")
    success_message = "Producto Editado Correctamente"
    permission_required = "products.change_product"

class ProductoDel(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    permission_required = "componentes.delete_product"
    model = Product
    template_name = "products/del.html"
    context_object_name = "obj"
    success_url= reverse_lazy("products:producto")
    success_message="Producto borrado satisfactoriamente"

def productosSinExistencia(request):
    sin_exis = Product.objects.filter(stock_inicial = '0')

    return render(request, 'products/sin_exis.html', {'sin_exis': sin_exis})