# admin_views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required(login_url='home')
@user_passes_test(is_admin)
@login_required(login_url='home')
@user_passes_test(is_admin)
def manage_users(request):
    # List all users and provide dashboard stats
    from .models import Usuarios
    usuarios = Usuarios.objects.all()
    usuarios_count = Usuarios.objects.count()
    usuarios_activos = Usuarios.objects.filter(verificado=1).count()
    total_coins = sum(u.metrocoins.balance for u in Usuarios.objects.all() if hasattr(u, 'metrocoins') and getattr(u.metrocoins, 'balance', None))
    context = {
        'usuarios': usuarios,
        'usuarios_count': usuarios_count,
        'usuarios_activos': usuarios_activos,
        'total_coins': total_coins,
    }
    return render(request, 'admin_manage_users.html', context)

@login_required(login_url='home')
@user_passes_test(is_admin)
def admin_ranking(request):
    return render(request, 'admin_ranking.html')

@login_required(login_url='home')
@user_passes_test(is_admin)
def admin_games(request):
    return render(request, 'admin_games.html')

@login_required(login_url='home')
def profile(request):
    return render(request, 'profile.html')
