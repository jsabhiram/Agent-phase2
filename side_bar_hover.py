# state_manager.py
side_flag = False

def get_side():
    global side_flag
    return side_flag

def change_side():
    global side_flag
    side_flag = not side_flag
