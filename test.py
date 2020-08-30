from model import Dnevnik
from datetime import date
import json

JSON_DATOTEKA = 'dnevnik.json'

prvi_dnevnik = Dnevnik.nalozi_stanje(JSON_DATOTEKA)

for album in prvi_dnevnik.seznam_albumov:
    print(album)

print(20 * '=')
 
def preveri():
    if prvi_dnevnik.seznam_albumov[0] < prvi_dnevnik.seznam_albumov[1]:
        print('da')
    else:
        print('ne')

preveri()

for album in prvi_dnevnik.sortiraj_po_abecedi():
    print(album)

print(20 * '=')
for album in prvi_dnevnik.sortiraj_po_izvajalcu('Taylor Swift'):
    print(album)

print(20 * '=')
for album in prvi_dnevnik.sortiraj_po_zanru('soul'):
    print(album)

print(20 * '=')
for album in prvi_dnevnik.sortiraj_po_abecedi():
    print(album)