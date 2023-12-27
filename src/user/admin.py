from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'email', 'is_staff')
    search_fields = ('phone_number', 'email')
    readonly_fields = ('id', 'registration_date')

    ordering = ('phone_number',)  # Remplacer 'username' par 'phone_number'

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'owner_name')  # Ajouter une méthode pour afficher le nom du propriétaire
    search_fields = ('name', 'phone_number', 'email')
    readonly_fields = ('id',)

    def owner_name(self, obj):
        return obj.owner.phone_number  # Ou toute autre attribut représentatif de l'utilisateur
    owner_name.short_description = 'Owner'



admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Riddle)
admin.site.register(RiddleToken)
