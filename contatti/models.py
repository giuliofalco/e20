from django.db import models

ARCHIVIO = (
             ('R','Ristoranti'),
             ('H','Hotel')
)

class Aziende(models.Model):
    archivio = models.CharField(max_length=2,default='R',blank=True,null=True,choices=ARCHIVIO) # R=ristorante v H=hotel
    categoria = models.CharField(max_length=150,null=True)
    nome = models.CharField(max_length=250)
    descrizione = models.TextField(null=True,blank=True)
    indirizzo = models.CharField(max_length=300, null=True)
    citta = models.CharField(max_length=200, null=True,blank=True)
    cap = models.CharField(max_length=6, null=True)
    provincia = models.CharField(max_length=4, null=True,blank=True)
    phone = models.CharField(max_length=200, null=True,blank=True)
    mail = models.EmailField(max_length=200, null=True,blank=True)
    web = models.URLField(max_length=200, null=True,blank=True)
    facebook = models.URLField(max_length=200, null=True,blank=True)
    twitter = models.URLField(max_length=200, null=True,blank=True)
    youtube = models.URLField(max_length=200, null=True,blank=True)
    num_immagini = models.IntegerField(default=0)
    servizi = models.TextField(null=True,blank=True)
    altri_servizi = models.TextField(null=True,blank=True)
    google_map = models.TextField(max_length=300, null=True,blank=True)
    orari = models.TextField(null=True,blank=True)

    def __str__(self):
       return(self.nome)
    
    class Meta:
        ordering = ['archivio','nome']
