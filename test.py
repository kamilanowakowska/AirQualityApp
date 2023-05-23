from my_functions import *
import pytest

"""Ten moduł zawiera testy modułu my_functions."""


#type "pytest test.py" to run tests

def test_lokalizator():
    loc = "Warszawa, Woronicza 17"
    promien = 30
    result = lokalizator(loc, promien)

    assert isinstance(result, list) == True

def test_dbinsert():
    db_insert()

        
