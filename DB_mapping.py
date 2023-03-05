# import obiektów z SQLAlchemy, których działanie zobaczymy z czasem 

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# inicjalizacja połaczenia z bazą danych 

engine = create_engine('sqlite:///powietrze.db', echo=True)


# obsluga zarządzania tabelami

base = declarative_base()

# definiowanie tabeli 'stacje_pomiarowe'

class StacjaPomiarowa(base):

    __tablename__ = 'stacje_pomiarowe'

    station = Column(Integer, primary_key=True )
    stationName = Column(String)
    gegrLat = Column(String)
    gegrLon = Column(String)
    loc_id = Column(Integer)
    addressStreet = Column(String)
    city_name = Column(String)
    communeName = Column(String)
    districtName = Column(String)
    provinceName = Column(String)
    sensors = relationship('StanowiskoPomiarowe', backref='stacje_pomiarowe')
    

    def __init__(self, station_data):
        self.station = station_data['id']
        self.stationName = station_data['stationName']
        self.gegrLat = station_data['gegrLat']
        self.gegrLon = station_data['gegrLon']
        self.loc_id = station_data['city']['id']
        self.addressStreet = station_data['addressStreet']
        self.city_name = station_data['city']['name']
        self.communeName = station_data['city']['commune']['communeName']
        self.districtName = station_data['city']['commune']['districtName']
        self.provinceName = station_data['city']['commune']['provinceName']


# definiowanie tabeli 'stanowiska_pomiarowe'

class StanowiskoPomiarowe(base):

    __tablename__ = 'stanowiska_pomiarowe'

    id = Column(Integer, primary_key=True )
    station_id = Column(Integer, ForeignKey('stacje_pomiarowe.station'))
    paramName = Column(String)
    paramFormula = Column(String)
    paramCode = Column(String)
    idParam = Column(Integer)
    measures = relationship('Pomiar', backref='stanowiska_pomiarowe')
    

    def __init__(self, sensor_data):
        self.id = sensor_data['id']
        self.station_id = sensor_data['stationId']
        self.paramName = sensor_data['param']['paramName']
        self.paramFormula = sensor_data['param']['paramFormula']
        self.paramCode = sensor_data['param']['paramCode']
        self.idParam = sensor_data['param']['idParam']


 # definiowanie tabeli 'pomiary'

class Pomiar(base):

    __tablename__ = 'pomiary'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('stanowiska_pomiarowe.id'))
    key = Column(String)
    date = Column(String)
    value = Column(Float)
    

    def __init__(self, sensor_id, key, date, value):
        self.sensor_id = sensor_id
        self.key = key
        self.date = date
        self.value = value  


# tworzenie tabel

base.metadata.create_all(engine)



