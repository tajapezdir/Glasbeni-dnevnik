import json

seznam_zanrov = []
with open('glasbene-zvrsti.txt', encoding='UTF-8') as datoteka:
    for zvrst in datoteka:
        seznam_zanrov.append(zvrst.strip())

seznam_ocen = list(range(1, 11))

    

class Dnevnik:
    def __init__(self):
        self.seznam_albumov = []
        self.seznam_izvajalcev = []
        self._seznam_letnic = []
        self._slovar_ocen = {} #slovar oblike {ocena: stevilo albumov s to oceno}
        self._izvajalci_z_naslovi = {} # slovar oblike {(izvajalec, naslov): Album}

    # def st_ponovljenih(self, izvajalec, naslov):
    #     st = 0
    #     for album in self.seznam_albumov:
    #         if naslov in album.naslov:
    #             if izvajalec == album.izvajalec:
    #                 st += 1
    #     return st 

    def preveri_album(self, izvajalec, naslov, opis):
        if izvajalec == '' or naslov == '' or opis == '':
            raise ValueError(
                f'Izpolniti morate vsa polja'
            )     
        elif (izvajalec, naslov) in self._izvajalci_z_naslovi:
            # stevilo = self.st_ponovljenih(izvajalec, naslov)
            raise ValueError(
                f'Ta album ste že vnesli'
            )
        
   
    def nov_album(self, naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis, st_vnosov=1):
        self.preveri_album(izvajalec, naslov, opis)
        nov_album = Album(naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis, self, st_vnosov)
        self.seznam_izvajalcev.append(izvajalec)
        self._izvajalci_z_naslovi[(izvajalec, naslov)] = nov_album
        self._seznam_letnic.append(leto_izdaje) 
        self.seznam_albumov.append(nov_album)
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
        for ocena, st in self._slovar_ocen.items():
            n += st
            vsota += ocena * st
        return round(vsota / n, 1)
                                        

    def sortiraj_po_abecedi(self): # moram še izboljšati, zaenkrat sortira samo po imenih izvajalcev
        seznam_po_abecedi = []
        if len(self.seznam_albumov) == 0:
            raise ValueError('Vnesli niste še nobenega albuma')        
        for izvajalec in sorted(self.seznam_izvajalcev):
            for album in self.seznam_albumov:
                if izvajalec == album.izvajalec:
                    seznam_po_abecedi.append(album)
        return seznam_po_abecedi
            

    def sortiraj_po_letu_izdaje(self):
        seznam_po_letnicah = []
        if len(self.seznam_albumov) == 0:
            raise ValueError('Vnesli niste še nobenega albuma')
        for letnica in sorted(self._seznam_letnic):
            for album in self.seznam_albumov:
                if letnica == album.leto_izdaje:
                    seznam_po_letnicah.append(album)
        return seznam_po_letnicah

    def sortiraj_po_zanru(self, zvrst):
        seznam_po_zanru = []
        if len(self.seznam_albumov) == 0:
            raise ValueError('Vnesli niste še nobenega albuma')
        for album in self.seznam_albumov:
            if zvrst == album.zvrst:
                seznam_po_zanru.append(album)
        return seznam_po_zanru

    def sortiraj_po_izvajalcu(self, izvajalec):
        seznam_po_izvajalcu = []
        if len(self.seznam_albumov) == 0:
            raise ValueError('Vnesli niste še nobenega albuma')  
        for album in self.seznam_albumov:
            if izvajalec == album.izvajalec:
                seznam_po_izvajalcu.append(album)
        return seznam_po_izvajalcu        

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


