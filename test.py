import requests
import sqlite3
from datetime import datetime
import pandas as pd
from tabulate import tabulate
import json
import numpy as np

def check_date(col=None):
    # Solo valida el formato; no pide más entradas
    if col == '' or col is None:
        return None  # Permite un valor nulo
    try:
        col = datetime.strptime(col, '%d-%m-%Y').date()
        return col
    except ValueError:
        return None  # Devuelve None si no es un número

check_date()