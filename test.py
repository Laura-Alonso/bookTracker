import requests
import sqlite3
from datetime import datetime
import pandas as pd
from tabulate import tabulate
import json
import numpy as np

def check_format(col = None):
    while True:
        if col == '' or col is None:
            return None  # Permite un valor nulo
        try:
            col = int(col)
            if col in (1,2):    
                return col
            else:
                 print("Introduzca 1 para Papel, 2 para Ebook.")
                 break                 
        except ValueError:
            print("Introduzca 1 para Papel, 2 para Ebook.")
            break     

check_format(3)