from django.shortcuts import render
from .models import Corso
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Corso, Prenotazione
from django.contrib import messages
from .models import Profile

def lista_corsi(request):
    corsi = Corso.objects.all()

    # Ricerca per prezzo massimo
    prezzo_max = request.GET.get('prezzo_max')
    if prezzo_max and prezzo_max.isdigit():
        corsi = corsi.filter(prezzo__lte=prezzo_max)

    # Ordinamento
    ordine = request.GET.get('ordine')
    if ordine == 'prezzo':
        corsi = corsi.order_by('prezzo')
    elif ordine == 'data':
        corsi = corsi.order_by('data')

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

    prenotazione_esistente = Prenotazione.objects.filter(
        utente=request.user,
        corso=corso,
        attiva=True
    ).exists()

    if prenotazione_esistente:
        messages.warning(request, "Sei già prenotata a questo corso.")

    elif corso.posti_disponibili == 0:
        messages.error(request, "Posti esauriti.")

    else:
        Prenotazione.objects.create(
            utente=request.user,
            corso=corso
        )
        corso.posti_disponibili -= 1
        corso.save()

        messages.success(request, "Prenotazione effettuata con successo!")

    return redirect('lista_corsi')
@login_required
def mie_prenotazioni(request):
    prenotazioni = Prenotazione.objects.filter(utente=request.user)

    return render(request, 'corsi/mie_prenotazioni.html', {
        'prenotazioni': prenotazioni
    })

@login_required
def annulla_prenotazione(request, prenotazione_id):
    prenotazione = get_object_or_404(
        Prenotazione,
        id=prenotazione_id,
        utente=request.user
    )

    corso = prenotazione.corso
    prenotazione.delete()

    corso.posti_disponibili += 1
    corso.save()

    messages.success(request, "Prenotazione annullata con successo.")

    return redirect('mie_prenotazioni')
    

@login_required
def modifica_profilo(request):
    profile = request.user.profile

    if request.method == 'POST':
        if 'immagine_profilo' in request.FILES:
            profile.immagine_profilo = request.FILES['immagine_profilo']
            profile.save()
            messages.success(request, "Immagine profilo aggiornata!")

        return redirect('modifica_profilo')

    return render(request, 'corsi/modifica_profilo.html')