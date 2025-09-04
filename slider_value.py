# state_manager.py
value = None

def get_value():
    global value
    return value

def change_value(x):
    global value
    value = x
    
    
