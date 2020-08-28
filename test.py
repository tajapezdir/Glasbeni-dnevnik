from model import Dnevnik
from datetime import date
import json

JSON_DATOTEKA = 'dnevnik.json'

prvi_dnevnik = Dnevnik()

prvi_dnevnik.nov_album(
    'Red',
    'Taylor Swift',
    date.today(),
    2012,
    'pop',
    8,
    'Vrhunec album doseže v pesmi All too well. Posebno se me je dotaknilo besedilo: "so casually cruel in the name of being honest"'
)

prvi_dnevnik.nov_album(
    'Two hands',
    'Big Thief',
    date.today(),
    2019,
    'indie',
    8,
    'forgotten eyes: "forgotten tongue is the language of love"'
)

prvi_dnevnik.nov_album(
    'I forget where we were',
    'Ben Howard',
    date.today(),
    2016,
    'folk',
    8,
    'sosledje pesmi End of the affair, Evergreen in Conrad'
)

prvi_dnevnik.nov_album(
    'Otis Blue/Otis Redding Sings Soul',
    'Otis Redding',
    date.today(),
    2016,
    'soul',
    8,
    'Na albumu je veliko priredb. Tiste, ki so originalne, pa so v kasnejših letih postale priredbe. Iztopa pesem Respet'
)

prvi_dnevnik.shrani_stanje(JSON_DATOTEKA)

print(prvi_dnevnik.stevilo_albumov())

for album in prvi_dnevnik.seznam_albumov:
    print(album.izvajalec + ' - ' + album.naslov)

