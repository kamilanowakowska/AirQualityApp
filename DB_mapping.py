# import obiektów z SQLAlchemy, których działanie zobaczymy z czasem 

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

import requests

# inicjalizacja połaczenia z bazą danych 

engine = create_engine('sqlite:///powietrze.db', echo=True)


# obsluga zarządzania tabelami

base = declarative_base()

class StacjaPomiarowe(base):

    __tablename__ = 'stacje_pomiarowe'

    station = Column(Integer, primary_key=True )
    stationName = Column(String)
    gegrLat = Column(Integer)
    gegrLon = Column(Integer)
    loc_id = Column(Integer)
    addressStreet = Column(String)
    city_name = Column(String)
    communeName = Column(String)
    districtName = Column(String)
    provinceName = Column(String)
    

    def __init__(self, station, stationName, gegrLat, gegrLon, loc_id, addressStreet, city_name, communeName, districtName, provinceName):
        self.station = station
        self.stationName = stationName
        self.gegrLat = gegrLat
        self.gegrLon = gegrLon
        self.loc_id = loc_id
        self.addressStreet = addressStreet
        self.city_name = city_name
        self.communeName = communeName
        self.districtName = districtName
        self.provinceName = provinceName

class StanowiskoPomiarowe(base):

    __tablename__ = 'stanowiska_pomiarowe'

    id = Column(Integer, primary_key=True )
    station_id = Column(Integer)
    paramName = Column(String)
    paramFormula = Column(String)
    paramCode = Column(String)
    idParam = Column(Integer)
    

    def __init__(self, id, station_id, paramName, paramFormula, paramCode, idParam):
        self.id = id
        self.station_id = station_id
        self.paramName = paramName
        self.paramFormula = paramFormula
        self.paramCode = paramCode
        self.idParam = idParam
     
class Pomiar(base):

    __tablename__ = 'pomiary'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    key = Column(String)
    date = Column(String)
    value = Column(Integer)
    

    def __init__(self, sensor_id, key, date, value):
        self.sensor_id = sensor_id
        self.key = key
        self.date = date
        self.value = value  


# tworzenie tabel

base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

res = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/findAll").json()


for station in res:
    stacja_pomiarowa = StacjaPomiarowe(station['id'], station['stationName'], station['gegrLat'], station['gegrLon'], station['city']['id'], station['addressStreet'], 
    station['city']['name'], station['city']['commune']['communeName'], station['city']['commune']['districtName'], station['city']['commune']['provinceName'])
    
    session.add(stacja_pomiarowa)

for station in res:
    res2 = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/sensors/{}".format(station['id'])).json()
    for sensor in res2:
        stanowisko_pomiarowe = StanowiskoPomiarowe(sensor['id'], sensor['stationId'], sensor['param']['paramName'], sensor['param']['paramFormula'],
        sensor['param']['paramCode'], sensor['param']['idParam'])

        session.add(stanowisko_pomiarowe)

        res3 = requests.get("https://api.gios.gov.pl/pjp-api/rest/data/getData/{}".format(sensor['id'])).json()
        for dana in res3['values']:
            pomiar = Pomiar(sensor['id'], res3['key'], dana['date'], dana['value'])

            session.add(pomiar)



   
session.commit()

