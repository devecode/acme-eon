from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm


@login_required(login_url = "users:login")
def home(request):
    from sales.models import VentaGeneral, VentaProducto
    from shopping.models import CompraGeneral, CompraProducto
    from products.models import Product
    from django.db.models import Count, Sum, Max, Min, F, FloatField
    from datetime import date, datetime, timedelta

 
    fecha = str(date.today())

    ventas = VentaGeneral.objects.count()
    total_ventas = VentaGeneral.objects.all().aggregate(Sum('total'))
    total_compras = CompraGeneral.objects.all().aggregate(Sum('total'))

    context = {'ventas': ventas, 'total_ventas': total_ventas, 'total_compras': total_compras}

    return render(request, 'users/inicio.html', context)


def registroUsuario(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'La cuenta de usuario a sido creada')

            login(request, user)
            return redirect('editar-cuenta')

        else:
            messages.success(
                request, 'Ah ocurrido un error durante el registro')

    context = {'form': form}
    return render(request, 'users/login_registro.html', context)


@login_required(login_url='users:login')
def cuentaUsuario(request):
    profile = request.user
    context = {'profile': profile}
    return render(request, 'users/cuenta.html', context)

@login_required(login_url='users:login')
def editarCuenta(request):
    profile = request.user
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('products:producto')
    

    context = {'form': form, 'profile': profile}
    return render(request, 'users/perfil_form.html', context)