from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registro/', views.registroUsuario, name="registro"),
    path('cuenta/', views.cuentaUsuario, name="cuenta"),
    path('editar-cuenta/', views.editarCuenta, name="editar-cuenta"),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),
                name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/login.html'),
            name='logout'),
]