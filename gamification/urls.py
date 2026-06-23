from django.urls import path
from . import views

urlpatterns = [
    # User routes
    path('', views.game_lobby, name='game_lobby'),
    path('perfil/', views.my_profile, name='my_profile'),
    path('ranking/', views.ranking, name='ranking'),
    
    path('cartas/', views.game_cartas, name='game_cartas'),
    path('submit/cartas/', views.submit_cartas, name='submit_cartas'),
    
    path('serpiente/', views.game_serpiente, name='game_serpiente'),
    path('submit/serpiente/', views.submit_serpiente, name='submit_serpiente'),
    
    path('ruleta/', views.game_ruleta, name='game_ruleta'),
    path('submit/ruleta/', views.submit_ruleta, name='submit_ruleta'),
    
    path('preguntas/', views.game_preguntas, name='game_preguntas'),
    path('submit/preguntas/', views.submit_preguntas, name='submit_preguntas'),

    # Admin routes
    path('admin/stats/', views.admin_stats, name='admin_stats'),
    path('admin/games/', views.admin_games, name='admin_games'),
]
