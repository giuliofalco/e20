#!/usr/bin/python3
from oop_pcto import *

# AGGIORNAMENTO DATABASE POSTGRES

#object = TutorImportPg('tutor.csv','mysite')
#object.aggiornaDb()

#for item in object.source.dati:
#    print(item)

#object = AziendeImportPg('aziende.tsv','mysite')
#object.aggiornaDb()

#for item in object.source.dati:
#    print(item)

# AGGIORNAMENTO DATABASE SQLITE

#object = AziendeImport('aziende.tsv','pcto.db')
#object.aggiornaDb()

object = Classi_tutorPg('classi_tutor','mysite')
object.aggiornaDb()

print ("Done")
