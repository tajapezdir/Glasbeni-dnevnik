import bottle
from model import Dnevnik, seznam_zvrsti, seznam_ocen
import json

from datetime import date

JSONOVA_DATOTEKA = 'dnevnik.json'

prvi_dnevnik = Dnevnik.nalozi_stanje(JSONOVA_DATOTEKA)

# POMOŽNE FUNKCIJE 

def _preveri_leto_izdaje(niz):
    try:
        int(niz)
    except:
        raise ValueError(f'Pri letu izdaje morate vnesti število!')

def _preveri_select(izbira):
    if izbira == None:
        raise ValueError('Morate izbrati eno izmed možnosti')

pomozni_slovar = {} # v ta slovar bom pod ključem 'spremenljivka' shranjevala izvajalca ali zvrst        

# GET DEKORATORJI

@bottle.get('/')
def osnovna_stran():
    bottle.redirect('/dnevnik/')

@bottle.get('/dnevnik/')
def zacetna_stran():
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=prvi_dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=prvi_dnevnik.seznam_albumov[::-1]
    )

@bottle.get('/dnevnik-po-abecedi/')
def dnevnik_po_abecedi():
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=prvi_dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=prvi_dnevnik.sortiraj_po_abecedi()
    )

@bottle.get('/dnevnik-po-letu/')
def dnevnik_po_letu():
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=prvi_dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=prvi_dnevnik.sortiraj_po_letu()
    )

@bottle.get('/dnevnik-po-izvajalcu/')
def dnevnik_po_izvajalcu():
    if len(pomozni_slovar) == 0:
        bottle.redirect('/')
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=prvi_dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=prvi_dnevnik.sortiraj_po_izvajalcu(pomozni_slovar['spremenljivka'])
    )

@bottle.get('/dnevnik-po-zvrsti/')
def dnevnik_po_zvrsti():
    if len(pomozni_slovar) == 0:
        bottle.redirect('/')
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=prvi_dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=prvi_dnevnik.sortiraj_po_zvrsti(pomozni_slovar['spremenljivka'])
    )

@bottle.get('/info/')
def info():
    return bottle.template('info.html')
    
# POST DEKORATORJI

@bottle.post('/dodaj-album/')
def nov_album():
    _preveri_leto_izdaje(bottle.request.forms.getunicode('leto izdaje'))
    _preveri_select(bottle.request.forms['zvrst'])
    _preveri_select(bottle.request.forms['ocena'])
    naslov = bottle.request.forms.getunicode('naslov')
    izvajalec = bottle.request.forms.getunicode('izvajalec')
    datum = date.today() 
    leto_izdaje = int(bottle.request.forms.getunicode('leto izdaje'))
    zvrst = bottle.request.forms['zvrst']
    ocena = int(bottle.request.forms['ocena'])
    opis = bottle.request.forms.getunicode('opis')
    prvi_dnevnik.nov_album(naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis)
    bottle.redirect('/')

@bottle.post('/sortiraj-po-datumu/')
def po_datumu():
    bottle.redirect('/')

@bottle.post('/sortiraj-po-abecedi/')
def po_abecedi():
    bottle.redirect('/dnevnik-po-abecedi/')

@bottle.post('/sortiraj-po-letu/')
def po_letu():
    bottle.redirect('/dnevnik-po-letu/')

@bottle.post('/sortiraj-po-izvajalcu/')
def po_izvajalcu():
    izvajalec = bottle.request.forms.getunicode('izvajalec')
    _preveri_select(izvajalec)
    pomozni_slovar['spremenljivka'] = izvajalec
    bottle.redirect('/dnevnik-po-izvajalcu/')

@bottle.post('/sortiraj-po-zvrsti/')
def po_zvrsti():
    zvrst = bottle.request.forms.getunicode('zvrst')
    _preveri_select(zvrst)
    pomozni_slovar['spremenljivka'] = zvrst
    bottle.redirect('/dnevnik-po-zvrsti/')

bottle.run(debug=True, reloader=True)
