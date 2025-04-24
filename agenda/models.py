from django.db import models
from django.contrib.auth.models import User


class Projects(models.Model):
    name = models.CharField(max_length=30)
    note = models.TextField(blank=True)
    def __str__(self):
        return self.name

class DayEntry(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date    = models.DateField(unique=False)   
    assenze = models.TextField(blank=True)   # docenti assenti
    eventi  = models.TextField(blank=True)   # eventi
    uscite  = models.TextField(blank=True)   # Classi in uscita
    note    = models.TextField(blank=True)   # Note varie
    updated_at = models.DateTimeField(auto_now=True)  # Data di ultimo aggiornamento
  
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
    
    def vuoto(self):
        # restituisce True quando i campi di testo sono tutti vuoti
        return not self.assenze and not self.eventi and not self.uscite and not self.note
    
    
class ProjectHours(models.Model):
    day_entry = models.ForeignKey('DayEntry', on_delete=models.CASCADE, related_name='project_hours')
    project = models.ForeignKey('Projects', on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.project.name} - {self.hours}h il {self.day_entry.date}"
 