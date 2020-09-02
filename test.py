from model import Dnevnik
from datetime import date

# v tej datoteki sem preizkušala delovanje modela

#logo = 
#    ______  ____    ____    ______  ______  ______  ____   _  ____  
#    |   ___||    |  |    \  |   ___||      >|   ___||    \ | ||    | 
#    |   |  ||    |_ |     \  `-.`-. |     < |   ___||     \| ||    | 
#    |______||______||__|\__\|______||______>|______||__/\____||____| 
#     _____   ____   _  ______  __    _ ____   _  ____  __  __        
#    |     \ |    \ | ||   ___|\  \  //|    \ | ||    ||  |/ /        
#    |      \|     \| ||   ___| \  \// |     \| ||    ||     \        
#    |______/|__/\____||______|  \__/  |__/\____||____||__|\__\       
                                                                     
JSON_DATOTEKA = 'dnevnik.json'

prvi_dnevnik = Dnevnik()

prvi_dnevnik.nov_album('Red', 'Taylor Swift', "2020-08-30", 2012, 'pop', 8, 'Verjetno najboljši album od Taylor Swift. Poln ljubezenskih balad in izjemen za v avto')
prvi_dnevnik.nov_album('Folklore', 'Taylor Swift', "2020-08-30", 2020, 'pop', 7, 'Album, ki je izšel med karanteno, vendar pa ima učinek pobega iz karantene')
prvi_dnevnik.nov_album('Teen Dream', 'Beach House', "2020-08-30", 2010, 'alternative', 8, 'Prvi Beach House album, ki sem ga poslušala. Zelo je umirjen, prijetno ga je poslušati med učenjem')
prvi_dnevnik.nov_album('Teen Dream', 'Beach House', "2020-09-02", 2010, 'alternative', 6, 'Hitro sem se ga naveličaka, saj je nekoliko dolgočasen')
prvi_dnevnik.nov_album('Talking Heads', 'Remain in Light', "2020-08-31", 1980, 'rock', 10, 'Zelo eksperimentalen album. Manj "dancey" kot njihovi prejšnji')
prvi_dnevnik.nov_album('Two Hands', 'Big Thief', "2020-08-30", 2019, 'indie', 8, 'Forgotten Eyes: "Forgotten tongue is the language of love"')
prvi_dnevnik.nov_album('I Forget Where we were', 'Ben Howard', "2020-08-30", 2016, 'folk', 10, 'Ob temu albumu vedno jokam. Najbolj udarno je sosledje pesmi: "Evergreen", "End of the affair" in "Conrad"')

for album in prvi_dnevnik.seznam_albumov:
    print(album)

print(20 * '=')
print(prvi_dnevnik.seznam_albumov[0])
print(prvi_dnevnik.seznam_albumov[1])

def preveri():
    if prvi_dnevnik.seznam_albumov[1] < prvi_dnevnik.seznam_albumov[0]:
        print('da')
    else:
        print('ne')

