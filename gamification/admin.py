from django.contrib import admin
from .models import GameConfig, UserMetroCoins, GameSession, RuletaSpin, Question

@admin.register(GameConfig)
class GameConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'coins_per_unit', 'max_coins_per_session', 'updated_at')
    list_editable = ('is_active', 'coins_per_unit', 'max_coins_per_session')

@admin.register(UserMetroCoins)
class UserMetroCoinsAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'total_earned', 'level')
    search_fields = ('user__username', 'level')

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_type', 'coins_earned', 'score', 'played_at')
    list_filter = ('game_type', 'played_at')
    search_fields = ('user__username',)
    readonly_fields = ('user', 'game_type', 'coins_earned', 'score', 'played_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(RuletaSpin)
class RuletaSpinAdmin(admin.ModelAdmin):
    list_display = ('user', 'fecha')
    search_fields = ('user__username',)
    list_filter = ('fecha',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('texto', 'respuesta_correcta', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('texto',)
