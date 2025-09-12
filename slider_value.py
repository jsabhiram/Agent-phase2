'''
# slider_value.py

This module contains functions and global variables for managing the slider value and overlay/notify states in the application.

## Global Variables

- [value](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/slider_value.py:13:0-15:16): A global variable that stores the current value of the slider.
- [sema](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/slider_value.py:48:0-52:16): A global variable that controls the semaphore for thread safety.
- `warning`: A global variable that stores the warning message.
- `show_warning`: A global variable that controls whether to show the warning message.
- [overlay_data](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/slider_value.py:77:0-79:23): A global variable that stores the data for the overlay/notify.
- `show_overlay`: A global variable that controls whether to show the overlay/notify.

## Functions

- [get_value()](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/slider_value.py:13:0-15:16): A function that returns the current value of the slider.
- [change_value(x)](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/slider_value.py:17:0-19:13): A function that sets the value of the slider to `x`.
- `get_warning()`: A function that returns the current warning message.
- `set_warning(x)`: A function that sets the warning message to `x`.
- `get_show_warning()`: A function that returns the current state of the warning display.
- `set_show_warning(x)`: A function that sets the state of the warning display to `x`.
- `get_overlay_data()`: A function that returns the current data for the overlay/notify.
- `set_overlay_data(x)`: A function that sets the data for the overlay/notify to `x`.
- `get_show_overlay()`: A function that returns the current state of the overlay/notify display.
- `set_show_overlay(x)`: A function that sets the state of the overlay/notify display to `x`.
- [change_sema()](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/slider_value.py:42:0-47:14): A function that toggles the state of the semaphore.
- [semaphore()](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/slider_value.py:48:0-52:16): A function that checks the state of the semaphore and returns `True` if it is set, `False` otherwise.
- [send_value(x, y, z=None)](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/slider_value.py:33:0-41:18): A function that sends the values `x` and `y` to the application, and optionally sets the overlay/notify data to `z`.

## Usage

To use this module, you can import the functions and global variables from `slider_value.py`. Here's an example:

```python
from slider_value import get_value, change_value, get_warning, set_warning, get_show_warning, set_show_warning, get_overlay_data, set_overlay_data, get_show_overlay, set_show_overlay, change_sema, semaphore, send_value

# Set the slider value
change_value(50)

# Get the current slider value
slider_value = get_value()

# Set the warning message
set_warning("Warning message")

# Get the current warning message
warning_message = get_warning()

# Toggle the warning display
set_show_warning(True)

# Get the current state of the warning display
is_warning_shown = get_show_warning()

# Set the overlay/notify data
set_overlay_data("Overlay data")

# Get the current data for the overlay/notify
overlay_data = get_overlay_data()

# Toggle the overlay/notify display
set_show_overlay(True)

# Get the current state of the overlay/notify display
is_overlay_shown = get_show_overlay()

# Send values to the application
send_value(10, 20)

# Check the state of the semaphore
is_sema_set = semaphore()

'''
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