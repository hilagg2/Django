import json
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum
from .models import GameConfig, UserMetroCoins, GameSession, RuletaSpin, Question

# --- USER VIEWS ---

@login_required(login_url='home')
def game_lobby(request):
    games = GameConfig.objects.all()
    # Asegurar que existan las configs
    for g in ['cartas', 'serpiente', 'ruleta', 'preguntas']:
        if not games.filter(name=g).exists():
            GameConfig.objects.create(name=g)
    
    games = GameConfig.objects.filter(is_active=True)
    metrocoins = getattr(request.user, 'metrocoins', None)
    
    return render(request, 'gamification/lobby.html', {
        'games': games,
        'metrocoins': metrocoins
    })

@login_required(login_url='home')
def my_profile(request):
    metrocoins = getattr(request.user, 'metrocoins', None)
    sessions = GameSession.objects.filter(user=request.user).order_by('-played_at')[:20]
    
    # Progreso de nivel
    levels = {'Bronce': 1000, 'Plata': 5000, 'Oro': 10000, 'Platino': 10000}
    current = metrocoins.total_earned if metrocoins else 0
    lvl = metrocoins.level if metrocoins else 'Bronce'
    next_goal = levels.get(lvl, 10000)
    progress = min(int((current / next_goal) * 100) if next_goal > 0 else 100, 100)

    return render(request, 'gamification/profile.html', {
        'metrocoins': metrocoins,
        'sessions': sessions,
        'progress': progress,
        'next_goal': next_goal
    })

@login_required(login_url='home')
def ranking(request):
    top_users = UserMetroCoins.objects.select_related('user').order_by('-total_earned')[:50]
    return render(request, 'gamification/ranking.html', {'top_users': top_users})

# -- JUEGOS --

@login_required(login_url='home')
def game_cartas(request):
    config = GameConfig.objects.filter(name='cartas', is_active=True).first()
    if not config: return redirect('game_lobby')
    return render(request, 'gamification/cartas.html', {'config': config})

@login_required(login_url='home')
def submit_cartas(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        parejas = int(data.get('parejas', 0))
        config = GameConfig.objects.get(name='cartas')
        
        coins = parejas * config.coins_per_unit
        coins = min(coins, config.max_coins_per_session)
        
        request.user.metrocoins.add_coins(coins)
        GameSession.objects.create(user=request.user, game_type='cartas', coins_earned=coins, score=parejas)
        
        return JsonResponse({'success': True, 'coins': coins})

@login_required(login_url='home')
def game_serpiente(request):
    config = GameConfig.objects.filter(name='serpiente', is_active=True).first()
    if not config: return redirect('game_lobby')
    return render(request, 'gamification/serpiente.html', {'config': config})

@login_required(login_url='home')
def submit_serpiente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        score = int(data.get('score', 0))
        config = GameConfig.objects.get(name='serpiente')
        
        coins = score * config.coins_per_unit
        coins = min(coins, config.max_coins_per_session)
        
        request.user.metrocoins.add_coins(coins)
        GameSession.objects.create(user=request.user, game_type='serpiente', coins_earned=coins, score=score)
        
        return JsonResponse({'success': True, 'coins': coins})

@login_required(login_url='home')
def game_ruleta(request):
    config = GameConfig.objects.filter(name='ruleta', is_active=True).first()
    if not config: return redirect('game_lobby')
    
    # Check si ya giró hoy
    ya_giro = RuletaSpin.objects.filter(user=request.user, fecha=timezone.now().date()).exists()
    return render(request, 'gamification/ruleta.html', {'config': config, 'ya_giro': ya_giro})

@login_required(login_url='home')
def submit_ruleta(request):
    if request.method == 'POST':
        hoy = timezone.now().date()
        if RuletaSpin.objects.filter(user=request.user, fecha=hoy).exists():
            return JsonResponse({'success': False, 'message': 'Ya giraste la ruleta hoy.'})
            
        data = json.loads(request.body)
        coins = int(data.get('coins', 0))
        config = GameConfig.objects.get(name='ruleta')
        coins = min(coins, config.max_coins_per_session)
        
        RuletaSpin.objects.create(user=request.user, fecha=hoy)
        request.user.metrocoins.add_coins(coins)
        GameSession.objects.create(user=request.user, game_type='ruleta', coins_earned=coins, score=coins)
        
        return JsonResponse({'success': True, 'coins': coins})

@login_required(login_url='home')
def game_preguntas(request):
    config = GameConfig.objects.filter(name='preguntas', is_active=True).first()
    if not config: return redirect('game_lobby')
    preguntas = list(Question.objects.filter(is_active=True))
    if len(preguntas) > 5:
        preguntas = random.sample(preguntas, 5)
    return render(request, 'gamification/preguntas.html', {'config': config, 'preguntas': preguntas})

@login_required(login_url='home')
def submit_preguntas(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        correctas = int(data.get('correctas', 0))
        config = GameConfig.objects.get(name='preguntas')
        
        coins = correctas * config.coins_per_unit
        coins = min(coins, config.max_coins_per_session)
        
        request.user.metrocoins.add_coins(coins)
        GameSession.objects.create(user=request.user, game_type='preguntas', coins_earned=coins, score=correctas)
        
        return JsonResponse({'success': True, 'coins': coins})

# --- ADMIN VIEWS ---

@staff_member_required(login_url='home')
def admin_stats(request):
    stats = GameSession.objects.values('game_type').annotate(
        total_plays=Count('id'),
        total_coins=Sum('coins_earned')
    ).order_by('-total_plays')
    
    return render(request, 'gamification/admin_stats.html', {'stats': stats})

@staff_member_required(login_url='home')
def admin_games(request):
    if request.method == 'POST':
        game_name = request.POST.get('game_name')
        is_active = request.POST.get('is_active') == 'on'
        coins_per_unit = request.POST.get('coins_per_unit')
        max_coins = request.POST.get('max_coins')
        
        g, created = GameConfig.objects.get_or_create(name=game_name)
        g.is_active = is_active
        if coins_per_unit: g.coins_per_unit = int(coins_per_unit)
        if max_coins: g.max_coins_per_session = int(max_coins)
        g.save()
        return redirect('admin_games')

    games = GameConfig.objects.all()
    # Default si no existen
    for g in ['cartas', 'serpiente', 'ruleta', 'preguntas']:
        if not games.filter(name=g).exists():
            GameConfig.objects.create(name=g)
            
    games = GameConfig.objects.all()
    return render(request, 'gamification/admin_games.html', {'games': games})
