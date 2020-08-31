import bottle
from model import Dnevnik, seznam_zanrov, seznam_ocen
import json

from datetime import date

JSONOVA_DATOTEKA = 'dnevnik.json'

prvi_dnevnik = Dnevnik.nalozi_stanje(JSONOVA_DATOTEKA)

# GET DEKORATORJI

@bottle.get('/')
def osnovna_stran():
    bottle.redirect('/dnevnik/')

@bottle.get('/dnevnik/')
def zacetna_stran():
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=prvi_dnevnik, 
        zvrsti=seznam_zanrov, 
        ocene=seznam_ocen
    )

@bottle.get('/analiza/')
def analiza():
    return bottle.template('analiza.html')

@bottle.get('/info/')
def info():
    return bottle.template('info.html')
    
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
