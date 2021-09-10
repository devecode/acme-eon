from django.urls import path
from .views import *

urlpatterns = [
    path('categoria',CategoriaList.as_view(), name='categoria'),
    path('categoria/nueva',CategoriaNew.as_view(), name='categoria_nueva'),
    path('categoria/edit/<int:pk>', CategoriaEdit.as_view(), name="categoria_edit"),
    path('categoria/delete/<int:pk>', CategoriaDel.as_view(), name='categoria_delete'),


    path('producto',ProductoList.as_view(), name='producto'),
    path('producto/nueva',ProductoNew.as_view(), name='producto_nuevo'),
    path('producto/edit/<int:pk>', ProductoEdit.as_view(), name="producto_edit"),
    path('producto/delete/<int:pk>', ProductoDel.as_view(), name='producto_delete'),


]
