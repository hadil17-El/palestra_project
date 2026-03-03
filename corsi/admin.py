from django.contrib import admin
from .models import Corso, Prenotazione


@admin.register(Corso)
class CorsoAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'data', 'posti_disponibili', 'prezzo')
    search_fields = ('titolo',)
    list_filter = ('data',)


@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ('utente', 'corso', 'data_prenotazione', 'attiva')
    list_filter = ('attiva',)