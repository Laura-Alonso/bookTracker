import requests
import sqlite3
from datetime import datetime
import pandas as pd
from tabulate import tabulate
import json
import numpy as np



# Date
def check_date(col=None):
    # Solo valida el formato; no pide más entradas
    if col == '' or col is None:
        return None  # Permite un valor nulo
    elif len(col) == 4:
        col2 = f"{col}-01-01"
    else:
        col2 = col
    try:
        col2 = datetime.strptime(col2, '%Y-%m-%d').date()
        return col2
    except ValueError:
        return None  # Devuelve None si no es un número
    
print(check_date("2024"))