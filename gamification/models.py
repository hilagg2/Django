from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class GameConfig(models.Model):
    GAME_CHOICES = [
        ('cartas', 'Cartas en Pareja'),
        ('serpiente', 'La Serpiente'),
        ('ruleta', 'Ruleta Diaria'),
        ('preguntas', 'Preguntas y Respuestas'),
    ]
    name = models.CharField(max_length=50, choices=GAME_CHOICES, unique=True)
    is_active = models.BooleanField(default=True)
    coins_per_unit = models.IntegerField(default=10, help_text="Monedas por acción (ej. por pareja, por respuesta)")
    max_coins_per_session = models.IntegerField(default=100, help_text="Límite de monedas por partida")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_name_display()

class UserMetroCoins(models.Model):
    LEVEL_CHOICES = [
        ('Bronce', 'Bronce'),
        ('Plata', 'Plata'),
        ('Oro', 'Oro'),
        ('Platino', 'Platino'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='metrocoins')
    balance = models.IntegerField(default=0)
    total_earned = models.IntegerField(default=0)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Bronce')

    def add_coins(self, amount):
        if amount > 0:
            self.balance += amount
            self.total_earned += amount
            self.update_level()
            self.save()

    def update_level(self):
        if self.total_earned >= 10000:
            self.level = 'Platino'
        elif self.total_earned >= 5000:
            self.level = 'Oro'
        elif self.total_earned >= 1000:
            self.level = 'Plata'
        else:
            self.level = 'Bronce'

    def __str__(self):
        return f"{self.user.username} - {self.balance} ₥"

# Signal para crear UserMetroCoins automáticamente
@receiver(post_save, sender=User)
def create_user_metrocoins(sender, instance, created, **kwargs):
    if created:
        UserMetroCoins.objects.create(user=instance)

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_sessions')
    game_type = models.CharField(max_length=50, choices=GameConfig.GAME_CHOICES)
    coins_earned = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game_type} - {self.coins_earned} ₥"

class RuletaSpin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'fecha')

    def __str__(self):
        return f"{self.user.username} - {self.fecha}"

class Question(models.Model):
    texto = models.TextField()
    opcion_a = models.CharField(max_length=100)
    opcion_b = models.CharField(max_length=100)
    opcion_c = models.CharField(max_length=100)
    opcion_d = models.CharField(max_length=100)
    
    RESPUESTAS = [
        ('A', 'Opción A'),
        ('B', 'Opción B'),
        ('C', 'Opción C'),
        ('D', 'Opción D'),
    ]
    respuesta_correcta = models.CharField(max_length=1, choices=RESPUESTAS)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.texto[:50]
