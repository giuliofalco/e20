from django.db import models

class Tutor(models.Model):
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    
    def __str__(self):
       return(f"{self.cognome} {self.nome}")
       
class Aziende(models.Model):
    partita_iva = models.CharField(max_length=80,null=True)
    ragione_sociale = models.CharField(max_length=200)
    tutor_referente_azienda = models.CharField(max_length=200,null=True)
    sede_comune = models.CharField(max_length=200,null=True)
    sede_provincia = models.CharField(max_length=20,null=True)
    telefono = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=100)
    settore = models.CharField(max_length=200,null=True)
    
    def __str__(self):
       return(self.ragione_sociale)
    
    class Meta:
        ordering = ['ragione_sociale']
