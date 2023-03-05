from Hamza_Demir_190701156_lab_8 import WebScrapper
import shelve

db_name = 'kitaplar.db'
ws = WebScrapper(db_name)
ws.parse()

with shelve.open(db_name, 'r') as db:
    for keys, values in db.items():
        print(keys, ':', values)
