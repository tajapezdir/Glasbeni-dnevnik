import json

seznam_zanrov = []
with open('glasbene-zvrsti.txt', encoding='UTF-8') as datoteka:
    for zvrst in datoteka:
        seznam_zanrov.append(zvrst.strip())
    

class Dnevnik:
    def __init__(self):
        self.seznam_albumov = []
        self.seznam_naslovov = []
        self._seznam_letnic = []
        self._izvajalci_z_naslovi = {} # slovar oblike {(izvajalec, naslov): Album}
  
   
    def nov_album(self, naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis):
        nov_album = Album(naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis, self)
        self.seznam_naslovov.append(naslov)
        self._izvajalci_z_naslovi[(izvajalec, naslov)] = nov_album
        self._seznam_letnic.append(leto_izdaje) 
        self.seznam_albumov.append(nov_album)
        return nov_album
    
    def stevilo_albumov(self):
        stevilo = 0
        for _ in self.seznam_albumov:
            stevilo += 1
        return stevilo

    def sortiraj_po_avtorju(self):
        return sorted(self.seznam_albumov)    

    def sortiraj_po_letu_izdaje(self):
        seznam_po_letnicah = []
        for letnica in self._seznam_letnic.sort():
            for album in self.seznam_albumov.sort():
                if letnica == album.leto_izdaje:
                    seznam_po_letnicah.append(album)
        return seznam_po_letnicah

    def sortiraj_po_zanru(self, zvrst):
        seznam_po_zanru = []
        for album in self.seznam_albumov.sort():
            if zvrst == album.zvrst:
                seznam_po_zanru.append(album)
        return seznam_po_zanru

    def izbrisi_album(self):
        pass


    def slovar_v_json(self):
        return {
            'albumi': [{
                'naslov': album.naslov,
                'izvajalec': album.izvajalec,
                'datum vnosa': str(album.datum),
                'leto izdaje': album.leto_izdaje,
                'zvrst': album.zvrst,
                'ocena': album.ocena,
                'opis': album.opis,       
            } for album in self.seznam_albumov],
        }
    
    @classmethod
    def nalozi_iz_jsona(cls, slovar_iz_json):
        dnevnik = cls()
        for album in slovar_iz_json['albumi']:
            dnevnik.nov_album(
                album['naslov'],
                album['izvajalec'],
                album['datum vnosa'],
                album['leto izdaje'],
                album['zvrst'],
                album['ocena'],
                album['opis'],                
            )
        return dnevnik
    
    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.slovar_v_json(), datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_iz_json = json.load(datoteka)
        return cls.nalozi_iz_jsona(slovar_iz_json)

class Album:
    def __init__(self, naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis, dnevnik):        
        self.naslov = naslov
        self.izvajalec = izvajalec
        self.datum = datum
        self.leto_izdaje = leto_izdaje
        self.zvrst = zvrst
        self.ocena = ocena
        self.opis = opis
        self.dnevnik = dnevnik

    def __lt__(self, other):
        if self.izvajalec == other.izvajalec:
            return self.naslov < other.naslov
        else: self.izvajalec < other.izvajalec


