from django.contrib import admin
from futbol.models import *

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInline(admin.TabularInline):
    model = Event
    extra = 2

class PartitAdmin(admin.ModelAdmin):
    # Resume lo ya esta guardado
    list_display = ("equip_local","equip_visitant","data","gols_local","gols_visitant")
    # Defines lo que quieres ver y poder modificar
    fields = ("lliga","equip_local","equip_visitant","data","gols_local","gols_visitant")
    # Abilita ver elemento no modificables de otros campos
    readonly_fields = ("gols_local","gols_visitant")
    # Añade un buscador
    search_fields = ("equip_local__nom","equip_visitant__nom")
    inlines = [EventInline]

admin.site.register(Partit, PartitAdmin)