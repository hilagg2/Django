'''Helper utilities para el sistema de gamificación del proyecto.'''

from .models import UserMetroCoins, GameConfig, GameSession
from django.contrib.auth.models import User

def award_coins(user: User, game_name: str, amount: int) -> None:
    """Agrega monedas al usuario por una partida.

    Crea un registro de GameSession y actualiza el balance de MetroCoins.
    """
    # Garantizo que exista la configuración del juego
    config = GameConfig.objects.get(name=game_name)
    # Registro la sesión
    GameSession.objects.create(
        user=user,
        game_type=game_name,
        coins_earned=amount,
        score=0,
    )
    # Actualizo el balance del usuario
    profile = user.metrocoins
    profile.add_coins(amount)

def get_leaderboard(limit: int = 10):
    """Devuelve los usuarios con mayor total de monedas ganadas.
    
    Ordenados de forma descendente y limitado a `limit` resultados.
    """
    return UserMetroCoins.objects.select_related('user').order_by('-total_earned')[:limit]
