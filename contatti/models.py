from django.db import models
from django.utils import timezone

ARCHIVIO = (
             ('R','Ristoranti'),
             ('H','Hotel'),
             ('G','Gelaterie'),
             ('C','Casse'),
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

class Agenti(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)
    
    def __str__(self):
       return(f"{self.cognome} {self.nome}")
    
    class meta:
        ordering = ['cognome','nome']

class Contatti(models.Model):
    data = models.DateField(default=timezone.now)
    azienda = models.ForeignKey(Aziende,on_delete=models.DO_NOTHING,null=True)
    agente = models.ForeignKey(Agenti,on_delete=models.CASCADE)
    note = models.TextField(null=True,blank=True)
    evidenziato = models.BooleanField(default=False)
    da_chimare = models.BooleanField(default=False)

    def __str__(self):
       return(self.data.strftime("%d/%m/%Y") + " " + self.agente.cognome)

    class Meta:
        ordering = ['-evidenziato','-data']

