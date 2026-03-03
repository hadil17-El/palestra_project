from django.db import models
from django.contrib.auth.models import User


class Corso(models.Model):
    titolo = models.CharField(max_length=100)
    descrizione = models.TextField()
    data = models.DateTimeField()
    posti_disponibili = models.PositiveIntegerField()
    prezzo = models.DecimalField(max_digits=6, decimal_places=2)
    immagine = models.ImageField(upload_to='corsi/', blank=True, null=True)

    def __str__(self):
        return self.titolo


class Prenotazione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    corso = models.ForeignKey(Corso, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField(auto_now_add=True)
    attiva = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.utente.username} - {self.corso.titolo}"