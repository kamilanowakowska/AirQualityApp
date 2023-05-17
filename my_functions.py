import pandas as pd
from DB_mapping import engine
from geopy.geocoders import Nominatim
from geopy.distance import distance
from sqlalchemy.orm import sessionmaker
import requests
from DB_mapping import engine, StacjaPomiarowa, StanowiskoPomiarowe, Pomiar
from datetime import date, timedelta

# połączenie SQLAlchemy 
cnx = engine.connect()


def lokalizator(loc, promien):
    """Znalezienie stacji pomiarowych w zadanym promieniu.
    
    Funkcja pobiera z bazy danych listę lokalizacji stacji pomiarowych.
    Następnie dla każdej stacji przeiczana jest odległość od zadanego punktu. 
    Jeśli odległość zawiera się w zadanym promieniu to stacja dodawana jest 
    do finalnej listy.
    
    :param loc: Adres wyszukiwania.
    :type loc: str
    :param loc: Promień wyszukiwania.
    :type loc: int
    :return: Lista stacji w zadanym promieniu od podanej lokalizacji.
    :rtype: list
    """

    geolocator = Nominatim(user_agent="my_request")
    location = geolocator.geocode(loc)
    location2 = location.latitude, location.longitude

    df2 = pd.read_sql_table('stacje_pomiarowe', cnx)
    df2 = df2[['gegrLat','gegrLon','stationName']]
    dict_of_loc = df2.to_dict('records')
    list_of_loc = []
    bliskie_loc = []

    for item in dict_of_loc:
        one_loc = item['gegrLat'], item['gegrLon'], item['stationName']
        list_of_loc.append(one_loc)
    
    for item in list_of_loc:
        item2 = item[0], item[1]
        km = distance(location2, item2)
        if km <= promien:
            bliskie_loc.append(item[2])
        
    return bliskie_loc



#databse update

def db_insert():
    """Dodanie nowych rekordów do bazy danych.
    
    Funkcja inentyfikuje rekordy, które istnieją już w bazie danych. 
    Następnie dla każdej tabeli pobierane są nowe rekordy.
    
    :return: Zapisanie nowych rekordów w bazie danych.
    """

    Session = sessionmaker(bind=engine)
    session = Session()

    stacje_pomiarowe_lista = []
    stanowiska_pomiarowe_lista = []
    pomiary_lista = [] 

    # utworzenie listy z aktualnie potencjalnie pokrywającymi się datami w bazie i API

    now = date.today()
    data_pomiaru1 = str(date.today())
    data_pomiaru2 = str(now - timedelta(days=1))
    data_pomiaru3 = str(now - timedelta(days=2))

    nowe_pomiary_lista =[data_pomiaru1, data_pomiaru2, data_pomiaru3]

    # utworzenie list identyfikujących istniejace rekordy dla każdej tabeli

    for s in session.query(StacjaPomiarowa).all():
        stacje_pomiarowe_lista.append(s.station)

    for s in session.query(StanowiskoPomiarowe).all():
        stanowiska_pomiarowe_lista.append(s.id)

    for s in session.query(Pomiar).all():
        filtr = s.date[:10]
        if filtr in nowe_pomiary_lista:
            pomiary_lista.append(s.date)


    pomiary_lista = list(dict.fromkeys(pomiary_lista))

    # sprawdzenie czy dane istnieją juz w bazie i zapisanie nowych rekordów

    res = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/findAll").json()


    for station in res:
        if station['id'] not in stacje_pomiarowe_lista:
            stacja_pomiarowa = StacjaPomiarowa(station)
                
            session.add(stacja_pomiarowa)
            

    for station in res:
        res2 = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/sensors/{}".format(station['id'])).json()

        for sensor in res2:
            if sensor['id'] not in stanowiska_pomiarowe_lista:
                stanowisko_pomiarowe = StanowiskoPomiarowe(sensor)

                session.add(stanowisko_pomiarowe)

                res3 = requests.get("https://api.gios.gov.pl/pjp-api/rest/data/getData/{}".format(sensor['id'])).json()
                for dana in res3['values']:
                    if dana['date'] not in pomiary_lista:
                        pomiar = Pomiar(sensor['id'], res3['key'], dana['date'], dana['value'])


            res3 = requests.get("https://api.gios.gov.pl/pjp-api/rest/data/getData/{}".format(sensor['id'])).json()
            for dana in res3['values']:
                if dana['date'] not in pomiary_lista:
                    pomiar = Pomiar(sensor['id'], res3['key'], dana['date'], dana['value'])

                    session.add(pomiar)

    return session.commit()

