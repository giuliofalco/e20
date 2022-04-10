from django.db import models

class Tutor(models.Model):
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    
    def __str__(self):
       return(f"{self.cognome} {self.nome}")
