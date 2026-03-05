from django.shortcuts import render
from .models import Corso
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Corso, Prenotazione
from django.contrib import messages
from .models import Profile
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

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

    else:
        # Se ci sono posti disponibili
        if corso.posti_disponibili > 0:
            Prenotazione.objects.create(
                utente=request.user,
                corso=corso,
                attiva=True,
                in_lista_attesa=False
            )

            corso.posti_disponibili -= 1
            corso.save()

            messages.success(request, "Prenotazione effettuata con successo!")

        # Se i posti sono finiti → lista d'attesa
        else:
            Prenotazione.objects.create(
                utente=request.user,
                corso=corso,
                attiva=False,
                in_lista_attesa=True
            )

            messages.info(request, "Posti esauriti. Sei stata inserita in lista d’attesa.")

    return redirect('lista_corsi')
@login_required
def mie_prenotazioni(request):

    prenotazioni_attive = Prenotazione.objects.filter(
        utente=request.user,
        attiva=True
    )

    prenotazioni_storico = Prenotazione.objects.filter(
        utente=request.user,
        attiva=False,
        in_lista_attesa=False
    )

    prenotazioni_lista_attesa = Prenotazione.objects.filter(
        utente=request.user,
        in_lista_attesa=True
    )

    # calcolo posizione lista attesa
    for pren in prenotazioni_lista_attesa:

        lista = Prenotazione.objects.filter(
            corso=pren.corso,
            in_lista_attesa=True
        ).order_by('data_prenotazione')

        posizione = list(lista).index(pren) + 1
        pren.posizione_lista = posizione

    return render(request, 'corsi/mie_prenotazioni.html', {
        'prenotazioni_attive': prenotazioni_attive,
        'prenotazioni_storico': prenotazioni_storico,
        'prenotazioni_lista_attesa': prenotazioni_lista_attesa
    })

@login_required
def annulla_prenotazione(request, prenotazione_id):

    prenotazione = get_object_or_404(
        Prenotazione,
        id=prenotazione_id,
        utente=request.user
    )

    corso = prenotazione.corso

    if prenotazione.attiva:

        prenotazione.attiva = False
        prenotazione.save()

        corso.posti_disponibili += 1
        corso.save()

        # cerca qualcuno in lista d'attesa
        prossimo = Prenotazione.objects.filter(
            corso=corso,
            in_lista_attesa=True
        ).order_by('data_prenotazione').first()

        if prossimo:

            prossimo.attiva = True
            prossimo.in_lista_attesa = False
            prossimo.save()

            corso.posti_disponibili -= 1
            corso.save()

            messages.info(
                request,
                "Un utente dalla lista d’attesa è stato promosso automaticamente."
            )

        messages.success(request, "Prenotazione annullata.")

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')