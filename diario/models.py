from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime
from datetime import date
from django.utils import timezone
from django.contrib import admin



def strdata(data):
    return str(data.day)+"/"+str(data.month)+"/"+str(data.year)

class Dieta(models.Model):
# il posto dove conservare la dieta, ogni oggetto è un giorno della settimana
    WEEKDAYS = ('lunedi','martedi','mercoledi','giovedi','venerdi','sabato','domenica')
    
    giorno = models.IntegerField(unique=True) # giorno della settimana 1 lun, 2 mar. ...
    note = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.giorno

    def wday(self):
        return WEEKDAYS[self.giorno]

class Diario(models.Model):
    WEEKDAYS = ('lunedi','martedi','mercoledi','giovedi','venerdi','sabato','domenica')
    
    data = models.DateField(default=date.today(),unique=True)
    note = models.CharField(max_length=200,blank=True, default="")
      
    class Meta:
        ordering = ['data']
      
    def __str__(self):
       return strdata(self.data) + " " + self.note
    
    def week_day(self):
    # restituisce il giorno della settimana sotto forma di stringa 
        wd = self.WEEKDAYS[self.data.isocalendar()[2]-1]
        return wd + " " + self.data.strftime("%d/%m/%Y")
        
    def w_day(self):
    # giorno della settimana come numero ISO 1=lun, 2=mar ... 7=dom
        wd = self.data.isocalendar()[2]
        return(wd)
        
    def week(self):
    # ritorna il numero della settimana ISO 
    # settimana che inizia il lunedì della prima settimana contenente il prox giov
    # fino a giovedì è il lunedi passato, da venerdi in avanti quello futuro
    # può partire dal 29 dic fino al 4 gennaio
        return self.data.isocalendar()[1]

class Alimento(models.Model):

    CATEGORIE = [(0,'Altro'),(1,'Latticini'),(2,'Cereali'),(3,'Pane'),(4,'Pasta'),(5,'Carni'),
                 (6,'Legumi'),(7,'Dolci'),(8,'Patate'),(9,'Bevande'),(10,'Pesce')]

    nome = models.CharField(max_length=50, unique=True)
    calorie = models.IntegerField(default=100)
    categoria = models.IntegerField(choices=CATEGORIE,default=0)
    
    def __str__(self):
       return self.nome
        
class Consumazione(models.Model):
    PASTI = [(0,'fuori_pasto'),(1,'colazione'),(2,'merenda_mat'),
             (3,'pranzo'),(4,'merenda_pom'),(5,'cena'),(6,'dopo_cena')]

    diario = models.ForeignKey(Diario,on_delete=models.CASCADE)
    tipo_pasto = models.IntegerField(choices=PASTI,default=0) 
    alimento = models.ManyToManyField(Alimento)
    acque = models.IntegerField(default=1)           # numero di bottigliette d'acqua consumate
    quantita_extra = models.BooleanField(default=False)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['tipo_pasto','diario'],name='pasto_unico')]
    
    def __str__(self):
       pasti = [pasto[1] for pasto in self.PASTI]
       return pasti[self.tipo_pasto]
    

