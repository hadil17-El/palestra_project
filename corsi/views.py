from django.shortcuts import render
from .models import Corso
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Corso, Prenotazione

def lista_corsi(request):
    corsi = Corso.objects.all()

    corsi_prenotati = []
    if request.user.is_authenticated:
        corsi_prenotati = Prenotazione.objects.filter(
            utente=request.user,
            attiva=True
        ).values_list('corso_id', flat=True)

    return render(request, 'corsi/lista_corsi.html', {
        'corsi': corsi,
        'corsi_prenotati': corsi_prenotati
    })

def registrazione(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registrazione.html', {'form': form})

@login_required
def prenota_corso(request, corso_id):
    corso = get_object_or_404(Corso, id=corso_id)

    # Controllo se l'utente ha già prenotato questo corso
    prenotazione_esistente = Prenotazione.objects.filter(
        utente=request.user,
        corso=corso,
        attiva=True
    ).exists()

    if not prenotazione_esistente and corso.posti_disponibili > 0:
        Prenotazione.objects.create(
            utente=request.user,
            corso=corso
        )
        corso.posti_disponibili -= 1
        corso.save()

    return redirect('lista_corsi')

@login_required
def mie_prenotazioni(request):
    prenotazioni = Prenotazione.objects.filter(utente=request.user)

    return render(request, 'corsi/mie_prenotazioni.html', {
        'prenotazioni': prenotazioni
    })

@login_required
def annulla_prenotazione(request, prenotazione_id):
    prenotazione = Prenotazione.objects.get(
        id=prenotazione_id,
        utente=request.user
    )

    corso = prenotazione.corso

    prenotazione.delete()

    corso.posti_disponibili += 1
    corso.save()

    return redirect('mie_prenotazioni')