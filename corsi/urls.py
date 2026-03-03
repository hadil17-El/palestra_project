from django.urls import path
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.lista_corsi, name='lista_corsi'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('prenota/<int:corso_id>/', views.prenota_corso, name='prenota_corso'),
    path('mie-prenotazioni/', views.mie_prenotazioni, name='mie_prenotazioni'),
    path('annulla/<int:prenotazione_id>/', views.annulla_prenotazione, name='annulla_prenotazione'),
    path('profilo/', views.modifica_profilo, name='modifica_profilo'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)