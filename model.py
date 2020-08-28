
seznam_zanrov = []
with open('glasbene-zvrsti.txt', encoding='UTF-8') as datoteka:
    for zvrst in datoteka:
        seznam_zanrov.append(zvrst.strip())
    

class Dnevnik:
    def __init__(self):
        self.seznam_albumov = []   
    
    def nov_album(self, naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis):
        nov = Album(naslov, izvajalec, datum, leto_izdaje, zvrst, ocena, opis, self)
        self.seznam_albumov.append(nov)
        return nov

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


