import bottle
from model import Dnevnik, seznam_zanrov
import json

from datetime import time

JSONOVA_DATOTEKA = 'dnevnik.json'

prvi_dnevnik = Dnevnik.nalozi_stanje(JSONOVA_DATOTEKA)

@bottle.get('/')
def zacetna_stran():
    return bottle.template('zacetna_stran.html', dnevnik=prvi_dnevnik)

# @bottle.post('/dodaj-album/')
# def dodaj_preliv():
#     znesek = int(bottle.request.forms['znesek'])
#     datum = date.today().strftime('%Y-%m-%d')
#     racun = poisci_racun('racun')
#     kuverta = poisci_kuverto('kuverta')
#     opis = bottle.request.forms.getunicode('opis')
#     proracun.nov_preliv(znesek, datum, opis, racun, kuverta)
#     shrani_trenutnega_uporabnika()
#     bottle.redirect('/')

bottle.run(debug=True, reloader=True)
