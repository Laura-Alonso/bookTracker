import requests
import sqlite3
from datetime import datetime
import pandas as pd
from tabulate import tabulate
import json
import numpy as np


def check_rate():
    while True:
        col = input("Rate the book (0-5 or leave empty): ")
        
        # Allow empty input to return None
        if col == '' or col is None:
            return None
        
        try:
            col = int(col)
            # Check if the number is within the valid range
            if col in (0, 1, 2, 3, 4, 5):
                return col  # Return valid rating
            else:
                print("Error: Enter a number between 0 and 5.")
        except ValueError:
            print("Error: Invalid input. Enter a number between 0 and 5.")

        

# Testing the function
print(check_rate())