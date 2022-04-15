#!/usr/bin/python3
from oop_pcto import *

# AGGIORNAMENTO DATABASE POSTGRES

#object = TutorImportPg('tutor.csv','mysite')
#object.aggiornaDb()

object = AziendeImportPg('aziende.tsv','mysite')
object.aggiornaDb()

# AGGIORNAMENTO DATABASE SQLITE

#object = AziendeImport('aziende.tsv','pcto.db')
#object.aggiornaDb()

print ("Done")
