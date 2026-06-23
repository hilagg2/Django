
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def game_lobby(request):
    return render(request, "gamify/lobby.html")

@login_required
def my_profile(request):
    return render(request, "gamify/profile.html")

def ranking(request):
    return render(request, "gamify/ranking.html")

@login_required
def game_cartas(request):
    return render(request, "gamify/game_cartas.html")

def submit_cartas(request):
    # placeholder for POST handling
    return render(request, "gamify/game_cartas.html")

@login_required
def game_serpiente(request):
    return render(request, "gamify/game_serpiente.html")

def submit_serpiente(request):
    return render(request, "gamify/game_serpiente.html")

@login_required
def game_ruleta(request):
    return render(request, "gamify/game_ruleta.html")

def submit_ruleta(request):
    return render(request, "gamify/game_ruleta.html")

@login_required
def game_preguntas(request):
    return render(request, "gamify/game_preguntas.html")

def submit_preguntas(request):
    return render(request, "gamify/game_preguntas.html")

@user_passes_test(lambda u: u.is_staff)
def admin_stats(request):
    return render(request, "gamify/admin_stats.html")

@user_passes_test(lambda u: u.is_staff)
def admin_games(request):
    return render(request, "gamify/admin_games.html")

