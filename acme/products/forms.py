from django import forms

from .models import Categorie, Product

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nombre']
        labels = {'nombre':"Nombre"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nombre', 'categoria', 'descripcion', 'precio', 'stock_inicial', 'stock_final']
        labels = {'nombre':"Nombre", 'categoria':"Categoría", 
                    'descripcion':"Descripción",'precio':"Precio", 'stock_inicial':"Stock Inicial",
                    'stock_final':"Stock Final"}
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })