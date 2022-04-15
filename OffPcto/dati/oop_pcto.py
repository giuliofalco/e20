#!/usr/bin/python3
import sqlite3

class Importa:
   # per caricare i dati da un file csv
            
   def __init__(self,nome_file):
       self.nome_file = nome_file     # il nome del file da importare
       self.csep = ','                # il carattere separatore
       self.campi = ""                # i nomi dei campi
       self.dati = self.carica_dati() # i dati come lista e l'intestazione con in nomi dei campi
       self.lower_nomi()              # capitalizza i nomi
   
   def lower_nomi(self):
       # sistema i cognomi e i nomi con la prima lettera maiuscola e il resto minuscolo
       for i in range(len(self.dati)):
           self.dati[i][1] = self.dati[i][1].capitalize()
           self.dati[i][2] = self.dati[i][2].capitalize()
       
   def get_email(self,nome,cognome):
       #restituisce la mail istituzionale del Mapelli, dati nome e cognome
       return(nome.lower() + "." + cognome.lower() + "@mapelli-monza.edu.it")
       
   def carica_dati(self):
      #  carica il file di dati, utilizza la prima riga per inizializzare l'intestazione
      #  prepara la lista dati ottenuta separando i campi, togliendo il fine stringa ed eliminando    
      #  l'intestazione
      
      f = open(self.nome_file,"r")
      listaRighe = f.readlines()    # legge tutte le righe del file e restituisce la lista delle righe
      f.close()                     # chiudo il file
      testa = listaRighe[0].strip() # memorizza in testa, la prima riga
      self.campi = testa.strip().split(self.csep)   # inizializza self.campi con la lista dei campi
      listaRighe = listaRighe[1:]   # toglie la prima riga da listaRighe
      return [item.strip().split(self.csep) for item in listaRighe] 
                                    # ritorna la lista con campi separati
          
   def togli_id(self):
     # toglie dai dati il primo campo id
     self.dati = [item[1:] for item in self.dati]
       
   def fill_data(self):
       # fill data with email and password
       for item in self.dati:
          item.append(self.get_email(item[1].lower(),item[0].lower()))
          item.append("Mapelli-2021")
          
class DbImport():
  # classe per aggiornare il database
  query="" # quesry generica da ridefinire nella classi figlie

  def __init__(self,fname,dbname):
       self.dbname = dbname          # nome del database
       self.source = Importa(fname)  # importa i dati dal file csv creando l'oggetto
       self.source.togli_id()        # elimina l'id
       self.source.fill_data()       # completa con email e password temporanea
  
  def connect(self):
      import sqlite3
      conn = sqlite3.connect(self.dbname)
      return conn
  
  def aggiornaDb(self):              # aggiorna il database utilizzando la query
      conn = self.connect()
      cur = conn.cursor()
      cur.executemany(self.query,self.source.dati)
      conn.commit()
      
class TutorImport(DbImport):
   # sottoclasse che specifica la query da utilizzare
   query = "INSERT INTO tutor (cognome,nome,email,password)  VALUES (?,?,?,?)"
   
class TutorImportPg(DbImport):
   # per connettersi al database su PostgreSQL tabella "OffPcto_tutor" di mysite usando con Django
   
   query = 'INSERT INTO "OffPcto_tutor" (cognome,nome,email) VALUES (%s,%s,%s)'
  
   def __init__(self,fname,dbname):
       super().__init__(fname,dbname)
       for item in self.source.dati:
           item.pop()  # tolgo la password dai dati
           
   def connect(self):
      import psycopg2
      #conn = psycopg2.connect(database="mysite", user="giulio", password="benoni58",host = "127.0.0.1")
      conn =  psycopg2.connect(dbname=d3034gq117jmk1 host=ec2-44-194-167-63.compute-1.amazonaws.com port=5432 user=yycpzjmtozwhci password=4b99951991961c1f66cd7f0f07dbe35972aa854164f9f7fc31b37237c3bc8827 sslmode=require)
      return conn
           
   
   
   
  
