from django.contrib import admin
from .models import Corso, Prenotazione, Profile
from django.utils.html import format_html

@admin.register(Corso)
class CorsoAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'data', 'posti_disponibili', 'prezzo')
    search_fields = ('titolo',)
    list_filter = ('data',)


@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ('utente', 'corso', 'data_prenotazione', 'attiva')
    list_filter = ('attiva',)

@admin.register(Profile)
class ProfiloAdmin(admin.ModelAdmin):
    list_display = ('user', 'anteprima')

    def anteprima(self, obj):
        return format_html('<img src="{}" width="50" />', obj.immagine_profilo.url)