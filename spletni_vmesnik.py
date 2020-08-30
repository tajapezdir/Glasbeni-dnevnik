import bottle
from model import Dnevnik, seznam_zanrov, seznam_ocen
import json

from datetime import date

JSONOVA_DATOTEKA = 'dnevnik.json'

prvi_dnevnik = Dnevnik.nalozi_stanje(JSONOVA_DATOTEKA)

# GET DEKORATORJI

@bottle.get('/')
def zacetna_stran():
    return bottle.template('zacetna_stran.html', dnevnik=prvi_dnevnik, zvrsti=seznam_zanrov, ocene=seznam_ocen)

# POST DEKORATORJI

@bottle.post('/dodaj-album/')
def nov_album():
    naslov = bottle.request.forms.getunicode('naslov')
    izvajalec = bottle.request.forms.getunicode('izvajalec')
    datum = date.today() 
    leto_izdaje = int(bottle.request.forms.getunicode('leto izdaje'))
    zvrst = bottle.request.forms.getunicode('zvrst')
    ocena = int(bottle.request.forms.getunicode('ocena'))
    opis = bottle.request.forms.getunicode('opis')
    prvi_dnevnik.nov_album(naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis)
    bottle.redirect('/')




bottle.run(debug=True, reloader=True)
