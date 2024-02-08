from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from relation.models import Point, Route, RepresentativePoint, RepresentativeRoute


# Register your models here.
class PointInline(admin.TabularInline):
    model = Point
    extra = 0  # N'ajoute pas de formulaires supplémentaires par défaut

class RouteInline(admin.StackedInline):
    model = Route
    extra = 0  # N'ajoute pas de formulaires supplémentaires par défaut
    inlines = [PointInline]  # Inclut les points associés à chaque trajet
    ordering = ("-departure",)  # Trie les trajets par date de départ, du plus récent au plus ancien
    
class RepresentativePointInline(admin.TabularInline):
    model = RepresentativePoint
    extra = 0  # N'ajoute pas de formulaires supplémentaires par défaut

class RepresentativeRouteInline(admin.StackedInline):
    model = RepresentativeRoute
    extra = 0  # N'ajoute pas de formulaires supplémentaires par défaut
    inlines = [RepresentativePointInline]  # Inclut les points associés à chaque trajet
    ordering = ("-departure",)  # Trie les trajets par date de départ, du plus récent au plus ancien

class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'registration_date')
    ordering = ('-registration_date',)  # Trie les utilisateurs par date d'inscription, du plus récent au plus ancien
    inlines = [RouteInline, RepresentativeRouteInline]  # Inclut les trajets associés à chaque utilisateur

# Enregistrement des modèles avec leurs classes ModelAdmin personnalisées


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')  # Ajouter une méthode pour afficher le nom du propriétaire
    search_fields = ('name', 'phone_number')
    readonly_fields = ('id',)

    def owner_name(self, obj):
        return f"{obj.get_owner().name } - {obj.get_owner().phone_number }" # Ou toute autre attribut représentatif de l'utilisateur
    owner_name.short_description = 'Owner'



admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Riddle)
admin.site.register(RiddleToken)
