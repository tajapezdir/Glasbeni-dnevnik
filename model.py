import json

seznam_zvrsti = []
with open('glasbene-zvrsti.txt', encoding='UTF-8') as datoteka:
    for zvrst in datoteka:
        seznam_zvrsti.append(zvrst.strip())

seznam_ocen = list(range(1, 11))

class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, dnevnik):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.dnevnik = dnevnik
    
    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            raise ValueError('Napačno geslo! Poskusite znova.')
    
    def shrani_stanje(self, ime_datoteke):
        slovar_stanja = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'zasifrirano_geslo': self.zasifrirano_geslo,
            'dnevnik': self.dnevnik.slovar_v_json()
        }
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            json.dump(slovar_stanja, datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_stanja = json.load(datoteka)
        uporabnisko_ime = slovar_stanja['uporabnisko_ime']
        zasifrirano_geslo = slovar_stanja['zasifrirano_geslo']
        dnevnik = Dnevnik.nalozi_iz_jsona(slovar_stanja['dnevnik'])
        return cls(uporabnisko_ime, zasifrirano_geslo, dnevnik)

class Dnevnik:
    def __init__(self):
        self.seznam_albumov = []
        self._seznam_izvajalcev = []
        self._seznam_letnic = []
        self._slovar_ocen = {} #slovar oblike {ocena: stevilo albumov s to oceno}
        self._izvajalci_z_naslovi = {} # slovar oblike {(izvajalec, naslov): Album}
        self.poslusane_zvrsti = []

    def stevilo_ponovjenih(self,izvajalec, naslov):
        album = self._izvajalci_z_naslovi[(izvajalec, naslov)]
        return album.st_vnosov + 1

    def stevilo_vnosov(self, izvajalec, naslov):
        if (izvajalec, naslov) in self._izvajalci_z_naslovi:
            return self.stevilo_ponovjenih(izvajalec, naslov)
        else:
            return 1

    def preveri_album(self, izvajalec, naslov, opis):
        if izvajalec == '' or naslov == '' or opis == '':
            raise ValueError(
                f'Izpolniti morate vsa polja'
            )      
   
    def nov_album(self, naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis):
        self.preveri_album(izvajalec, naslov, opis)
        st_vnosov = self.stevilo_vnosov(izvajalec.strip(), naslov.strip())
        nov_album = Album(naslov.strip(), izvajalec.strip(), datum, leto_izdaje, zvrst, ocena, opis, self, st_vnosov)
        self._seznam_izvajalcev.append(izvajalec.strip())
        self._izvajalci_z_naslovi[(izvajalec.strip(), naslov.strip())] = nov_album
        self._seznam_letnic.append(leto_izdaje) 
        self.seznam_albumov.append(nov_album)
        self.poslusane_zvrsti.append(zvrst)
        self._slovar_ocen[ocena] = self._slovar_ocen.get(ocena, 0) + 1 
        return nov_album
    
    def stevilo_albumov(self):
        stevilo = 0
        for _ in self.seznam_albumov:
            stevilo += 1
        return stevilo

    def povprecna_ocena(self):
        vsota = 0
        n = 0
        if len(self._slovar_ocen) == 0:
            return 0
        else:
            for ocena, st in self._slovar_ocen.items():
                n += st
                vsota += ocena * st
            return round(vsota / n, 1)                               

    def sortiraj_po_abecedi(self): # moram še izboljšati, zaenkrat sortira samo po imenih izvajalcev
        seznam_po_abecedi = []
        if len(self.seznam_albumov) == 0:
            raise ValueError('Vnesli niste še nobenega albuma')        
        for izvajalec in sorted(self._seznam_izvajalcev):
            for album in self.seznam_albumov:
                if izvajalec == album.izvajalec:
                    seznam_po_abecedi.append(album)
        return seznam_po_abecedi            

    def sortiraj_po_letu(self):
        seznam_po_letih = []
        if len(self.seznam_albumov) == 0:
            raise ValueError('Vnesli niste še nobenega albuma')
        for letnica in sorted(self._seznam_letnic):
            for album in self.seznam_albumov:
                if letnica == album.leto_izdaje:
                    seznam_po_letih.append(album)
        return seznam_po_letih

    def sortiraj_po_zvrsti(self, zvrst):
        seznam_po_zvrsti = []
        if len(self.seznam_albumov) == 0:
            raise ValueError('Vnesli niste še nobenega albuma')
        for album in self.seznam_albumov:
            if zvrst == album.zvrst:
                seznam_po_zvrsti.append(album)
        return seznam_po_zvrsti

    def sortiraj_po_izvajalcu(self, izvajalec):
        seznam_po_izvajalcu = []
        if len(self.seznam_albumov) == 0:
            raise ValueError('Vnesli niste še nobenega albuma')  
        for album in self.seznam_albumov:
            if izvajalec.upper() == album.izvajalec.upper():
                seznam_po_izvajalcu.append(album)
        return seznam_po_izvajalcu        

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
        with open(ime_datoteke, encoding='UTF-8') as datoteka:
            slovar_iz_json = json.load(datoteka)
        return cls.nalozi_iz_jsona(slovar_iz_json)

class Album:
    def __init__(self, naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis, dnevnik, st_vnosov):        
        self.naslov = naslov
        self.izvajalec = izvajalec
        self.datum = datum
        self.leto_izdaje = leto_izdaje
        self.zvrst = zvrst
        self.ocena = ocena
        self.opis = opis
        self.dnevnik = dnevnik
        self.st_vnosov = st_vnosov

    def __str__(self):
        return f'{self.izvajalec}: {self.naslov}, izdan leta {self.leto_izdaje}'

    def __lt__(self, other):
        if self.izvajalec == other.izvajalec:
            return self.naslov < other.naslov
        else: self.izvajalec < other.izvajalec


