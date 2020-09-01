import bottle
import random
import os
import hashlib
from model import Uporabnik, Dnevnik, seznam_zvrsti, seznam_ocen

from datetime import date

imenik_s_podatki = 'uporabniki'
uporabniki = {}
skrivnost = 'TO JE ENA HUDA SKRIVNOST'

if not os.path.isdir(imenik_s_podatki):
    os.mkdir(imenik_s_podatki)

for ime_datoteke in os.listdir(imenik_s_podatki):
    uporabnik = Uporabnik.nalozi_stanje(os.path.join(imenik_s_podatki, ime_datoteke))
    uporabniki[uporabnik.uporabnisko_ime] = uporabnik

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=skrivnost)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
    return uporabniki[uporabnisko_ime]

def dnevnik_uporabnika():
    return trenutni_uporabnik().dnevnik

def shrani_trenutnega_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.shrani_stanje(os.path.join('uporabniki', f'{uporabnik.uporabnisko_ime}.json'))

# JSONOVA_DATOTEKA = 'dnevnik.json'

# prvi_dnevnik = Dnevnik.nalozi_stanje(JSONOVA_DATOTEKA)

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

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.get('/')
def osnovna_stran():
    bottle.redirect('/dnevnik/')

@bottle.get('/dnevnik/')
def zacetna_stran():
    dnevnik = dnevnik_uporabnika()
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=dnevnik.seznam_albumov[::-1]
    )

@bottle.get('/dnevnik-po-abecedi/')
def dnevnik_po_abecedi():
    dnevnik = dnevnik_uporabnika()
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=dnevnik.sortiraj_po_abecedi()
    )

@bottle.get('/dnevnik-po-letu/')
def dnevnik_po_letu():
    dnevnik = dnevnik_uporabnika()
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=dnevnik.sortiraj_po_letu()
    )

@bottle.get('/dnevnik-po-izvajalcu/')
def dnevnik_po_izvajalcu():
    dnevnik = dnevnik_uporabnika()
    if len(pomozni_slovar) == 0:
        bottle.redirect('/')
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=dnevnik.sortiraj_po_izvajalcu(pomozni_slovar['spremenljivka'])
    )

@bottle.get('/dnevnik-po-zvrsti/')
def dnevnik_po_zvrsti():
    dnevnik = dnevnik_uporabnika()
    if len(pomozni_slovar) == 0:
        bottle.redirect('/')
    return bottle.template(
        'glasbeni_dnevnik.html', 
        dnevnik=dnevnik, 
        zvrsti=seznam_zvrsti, 
        ocene=seznam_ocen,
        albumi=dnevnik.sortiraj_po_zvrsti(pomozni_slovar['spremenljivka'])
    )

@bottle.get('/info/')
def info():
    return bottle.template('info.html')
    
# POST DEKORATORJI

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding='utf-8'))
    zasifrirano_geslo = h.hexdigest()
    if 'nov_racun' in bottle.request.forms and uporabnisko_ime not in uporabniki:
        uporabnik = Uporabnik(
            uporabnisko_ime,
            zasifrirano_geslo,
            Dnevnik()
        )
        uporabniki[uporabnisko_ime] = uporabnik
    else:
        uporabnik = uporabniki[uporabnisko_ime]
        uporabnik.preveri_geslo(zasifrirano_geslo)
    bottle.response.set_cookie('uporabnisko_ime', uporabnik.uporabnisko_ime, path='/', secret=skrivnost)
    bottle.redirect('/')

@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')

@bottle.post('/dodaj-album/')
def nov_album():
    dnevnik = dnevnik_uporabnika()
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
    dnevnik.nov_album(naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis)
    shrani_trenutnega_uporabnika()
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
