from django.contrib import admin
from costcenter.models import Cards, Transaction, Distribution,UserProfile,Acreditaciones
from .models import Consumo
from django.contrib.auth.models import User

# Filtro personalizado por Usuario
class UserFilter(admin.SimpleListFilter):
    title = 'User'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        return [(user.id, user.username) for user in User.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__id=self.value())
        return queryset

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "unit")    

@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ("user", "is_costcenter", "card_name", "money", 'card_number')
    list_filter = ("is_costcenter", 'user')  # Añade filtro por usuario
    search_fields = ("card_name", "user__username")  # Búsqueda por nombre de tarjeta y usuario
    exclude = ('card_number',)
    ordering = ('user', 'card_name')  # Ordena por usuario y nombre de tarjeta

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si está editando un objeto existente
            return self.readonly_fields + ('is_costcenter',)
        return self.readonly_fields


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'from_account', 'to_account', 'amount', 'distribution_date')
    search_fields = ('from_account', 'to_account', 'user__username')  # Añade búsqueda por usuario
    list_filter = ('distribution_date', UserFilter)  # Filtro por fecha y usuario
    ordering = ('user', 'from_account', 'distribution_date')  # Ordena por usuario, tarjeta y fecha


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'movement_date', 'from_account', 'to_account', 'amount')
    search_fields = ('from_account', 'to_account', 'user__username')  # Añade búsqueda por usuario
    list_filter = ('movement_date', UserFilter)  # Filtro por fecha y usuario
    ordering = ('user', 'from_account', 'movement_date')  # Ordena por usuario, tarjeta y fecha


@admin.register(Consumo)
class ConsumoAdmin(admin.ModelAdmin):
    list_display = ( 'consumo_id','user', 'card', 'establecimiento', 'importe', 'consumo_date')
    search_fields = ('consumo_id', 'establecimiento', 'card__user__username')  # Añade búsqueda por usuario
    list_filter = ('consumo_date', UserFilter, 'card')  # Filtro por fecha, usuario y tarjeta
    ordering = ('card__user', 'card', 'consumo_date')  # Ordena por usuario, tarjeta y fecha
    

    # Propiedad personalizada para mostrar el usuario en la lista
    def user(self, obj):
        return obj.card.user
    user.short_description = 'User'
    user.admin_order_field = 'card__user__username'  # Permite ordenar por usuario



@admin.register(Acreditaciones)
class AcreditacionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'importe', 'fecha_hora', 'card')
    search_fields = ('id',)