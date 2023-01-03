import sqlite3
import psycopg2
queryLettura = "SELECT categoria, nome, descrizione, indirizzo, citta, cap, provincia, phone, mail, web, facebook, twitter, num_immagini, servizi, altri_servizi, googlemap, orari FROM hotel;"
query = "INSERT INTO contatti_aziende (categoria, nome, descrizione, indirizzo, citta, cap, provincia, phone, mail, web, facebook, twitter, num_immagini, servizi, altri_servizi, google_map, orari ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

# lettura dei dati da SQLite

conn = sqlite3.connect('monza.db') # connessione a sqlite della sorgente di dati
cur = conn.cursor()
cur.execute(queryLettura)
dati = cur.fetchall()

# scrittura su PostgreSQL

conn = psycopg2.connect(database="e20", user="giulio", password="benoni58",host = "127.0.0.1") 

cur = conn.cursor()

#for tupla in dati:
#   # print(tupla)
#   for elem in tupla:
#       if isinstance(elem,int):
#          print(0, end=' ')   
#       else:
#          print (len(elem), end=' ')      
#   print()

cur.executemany(query,dati)
conn.commit()
print ('Done')

