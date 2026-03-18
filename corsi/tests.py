from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Corso, Prenotazione
from django.urls import reverse
from datetime import date

#TEST 1 — Creazione corso:Questo test controlla che un corso venga salvato nel database.
class CorsoModelTest(TestCase):

    def test_creazione_corso(self):
        corso = Corso.objects.create(
            titolo="Yoga Test",
            descrizione="Corso di yoga",
            data=date.today(),
            posti_disponibili=10,
            prezzo=20,
            tipologia="Yoga"
        )

        self.assertEqual(corso.titolo, "Yoga Test")
        self.assertEqual(corso.posti_disponibili, 10)

#TEST 2 — Prenotazione corso:Questo test verifica che un utente possa prenotare un corso.
class PrenotazioneTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )

        self.corso = Corso.objects.create(
            titolo="Pilates",
            descrizione="Corso pilates",
            data=date.today(),
            posti_disponibili=5,
            prezzo=15,
            tipologia="Pilates"
        )

    def test_prenotazione_corso(self):

        self.client.login(username="testuser", password="12345")

        response = self.client.get(
            reverse('prenota_corso', args=[self.corso.id])
        )

        self.assertEqual(response.status_code, 302)

        prenotazione = Prenotazione.objects.filter(
            utente=self.user,
            corso=self.corso
        ).exists()

        self.assertTrue(prenotazione)
        
#TEST 3 — Annullamento prenotazione
class AnnullaPrenotazioneTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )

        self.corso = Corso.objects.create(
            titolo="Crossfit",
            descrizione="Allenamento intenso",
            data=date.today(),
            posti_disponibili=5,
            prezzo=25,
            tipologia="Fitness"
        )

        self.prenotazione = Prenotazione.objects.create(
            utente=self.user,
            corso=self.corso,
            attiva=True
        )

    def test_annulla_prenotazione(self):

        self.client.login(username="testuser", password="12345")


        response = self.client.get(
            reverse('annulla_prenotazione', args=[self.prenotazione.id])
        )
        self.assertEqual(response.status_code, 302)
        self.prenotazione.refresh_from_db()

        self.assertFalse(self.prenotazione.attiva)