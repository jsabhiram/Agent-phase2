# state_manager.py
value = None
sema=False
import time
warning=None
show_warning=False

# New globals for overlay/notify
overlay_data = 'Nothing to show yet'
show_overlay = False


# status=False
def get_value():
    global value
    return value

def change_value(x):
    global value
    value = x
# def wait_for_user():                 #warning
    # global status
    # while(status!=False):
        # time.sleep(0.5)

def get_warning():   #warning
    global warning
    global show_warning
    lst=[show_warning,warning]
    return lst
# def get_status():            #warning
    # global status
    # return status
def send_value(x,y,z=None):
    
    global warning
    global show_warning
    if z!= None:
        man_overlay_data(z)
    change_sema()
    warning=y
    show_warning=x
def change_sema():
    global sema
    if sema:
        sema=False
        return
    sema =True
def semaphore():
    global sema
    if sema:
        return True
    return False





#-------------------finalizing---------------------------------------
# ------------------- New overlay functions -------------------
def set_overlay(data, status=True):
    """
    Set the overlay data and visibility.
    data: string to display in overlay
    status: True -> show overlay, False -> hide overlay
    """
    global overlay_data, show_overlay
    overlay_data = data
    show_overlay = status

def get_overlay():
    """
    Get current overlay status and data.
    Returns a tuple: (show_overlay, overlay_data)
    """
    global overlay_data, show_overlay
    return show_overlay, overlay_data
def man_overlay_data(data):
    global overlay_data
    overlay_data = data
def hide_overlay():
    """
    Hide the overlay without changing the data.
    """
    global show_overlay
    show_overlay = False

if __name__ == '__main__':
    # print(x:=get_warning())
    # send_value(True,"Warning triggered")
    # print(x:=get_warning())
    while True:
        # time.sleep(3)
        
        print(c:=show_warning)