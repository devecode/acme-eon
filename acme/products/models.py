from django.db import models
#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Categorie(models.Model):
    TIPO = (
        ('ABARROTES', 'ABARROTES'),
        ('ELECTRONICA', 'ELECTRONICA'),
        ('FARMACIA', 'FARMACIA'),
    )
    nombre = models.CharField('Categoría', max_length=80, choices=TIPO)

    def __str__(self):
        return self.nombre

class Product(models.Model):
    nombre = models.CharField('Nombre del Producto', max_length=200)
    descripcion = models.TextField('Descripción del Producto')
    precio = models.FloatField(default=0)
    categoria = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    stock_inicial = models.IntegerField(default=0)
    stock_final = models.IntegerField(default=0)

    def __str__(self):
        return '{}:{}'.format(self.nombre,self.descripcion)
