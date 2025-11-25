from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from salud.models import AdministradorEPS

class PrincipalView(View):
    def get(self, request):
        return render(request, 'home.html')


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        cedula = request.POST.get('cedula')
        password = request.POST.get('password')

        if not cedula or not password:
            messages.error(request, '⚠️ Por favor completa todos los campos')
            return redirect('login')

        try:
            # Buscar al administrador por cédula
            admin = AdministradorEPS.objects.get(numero_documento=cedula)
            user = admin.user
        except AdministradorEPS.DoesNotExist:
            messages.error(request, '⚠️ No existe un administrador con esa cédula')
            return redirect('login')

        # Verificar contraseña del usuario base
        if user.check_password(password):
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, '⚠️ Contraseña incorrecta')
            return redirect('login')




class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, '✓ Has cerrado sesión exitosamente')
        return redirect('login')