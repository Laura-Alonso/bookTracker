from datetime import datetime

# Isbn
def check_isbn(col = None):
    if col == '' or col is None:
       return None  
    try:
        col = int(col)
        if len(str(col)) == 13:    
            return col
        else:
            col = "Wrong input"
            return col                
    except ValueError:
        return None

# Date
def check_date(col=None):
    if col == '' or col is None:
        return None 
    elif len(col) == 4:
        col2 = f"{col}-01-01"
    else:
        col2 = col
    try:
        col2 = datetime.strptime(col2, '%Y-%m-%d').date()
        return col2
    except ValueError:
        return "Wrong input" 
    
# String (title, authors, description, gender, preview_link, image_lin)
def check_string(col = None):
    if col == "" or col is None:
        return None
    try:
        if col == str(col):
            return str(col)
        else:
            return "Wrong input" 
    except ValueError:
         return None

# Integer (page_count, times_readed)
def check_integer(col = None):
    if col == '' or col is None:
        return None  # Permite un valor nulo 
    try:
        col = int(col)
        return col
    except ValueError:
        return "Wrong input" 


# Format
def check_format(col = None):
    if col == '' or col is None:
        return None  # Permite un valor nulo
    try:
        col = int(col)
        if col in (1,2):    
           return col 
        else:
            return "Wrong input"            
    except ValueError:
        return "Wrong input" 

 

# Rate    
def check_rate(col=None):
    if col == '' or col is None:
        return None
    try:
        col = int(col)
        if col in (1, 2, 3, 4, 5):
            return col  # Return valid rating
        else:
            col = "Wrong input"
            return col
    except ValueError:
        return "Wrong input"