from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    in_lista_attesa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utente.username} - {self.corso.titolo}"
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    immagine_profilo = models.ImageField(
        upload_to='profili/',
        default='profili/default.png'
    )

    def __str__(self):
        return self.user.username


# Creazione automatica profilo quando si registra un utente
@receiver(post_save, sender=User)
def crea_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


#hadil17
#Had_jed17

##hadil(superuser)
###hadil