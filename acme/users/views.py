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