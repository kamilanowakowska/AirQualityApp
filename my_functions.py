import pandas as pd
from DB_mapping import engine
from geopy.geocoders import Nominatim
from geopy.distance import distance

import matplotlib.pyplot as plt

from sqlalchemy.orm import sessionmaker
import requests
from DB_mapping import engine, StacjaPomiarowa, StanowiskoPomiarowe, Pomiar
from datetime import date, timedelta

# połączenie SQLAlchemy 
cnx = engine.connect()

# wywołanie wyników dla konkretnej stacji pomiarowej

#średnie wartości w rozpatrywanym okresie
def sensor_results_mean(station_id):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    mean_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='mean')
    return mean_df



#najmniejsze wartości w rozpatrywanym okresie
def sensor_results_min(station_id):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    min_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='min')
    return min_df

#największe wartości w rozpatrywanym okresie
def sensor_results_max(station_id):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    max_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='max')
    return max_df



###########################################################################

#lokalizowanie wyszukiwania
def lokalizator(loc, promien):

    geolocator = Nominatim(user_agent="my_request")
    location = geolocator.geocode(loc)
    location2 = location.latitude, location.longitude

# zwraca listę stacji(gegrLat, gegrLon, stationName) w podanym promieniu[km] od podanej lokalizacji w lokalizatorze

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


##############################################################################


#databse update

def db_insert():

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

                        session.add(pomiar)
            else:
                res3 = requests.get("https://api.gios.gov.pl/pjp-api/rest/data/getData/{}".format(sensor['id'])).json()
                for dana in res3['values']:
                    if dana['date'] not in pomiary_lista:
                        pomiar = Pomiar(sensor['id'], res3['key'], dana['date'], dana['value'])

                        session.add(pomiar)

    return session.commit()

