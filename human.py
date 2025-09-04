def get_user_input():
    from app import get_slider_value
    slider_value = get_slider_value()
    return slider_value

import time


def waiting(state):
    time.sleep(3)
    if(get_user_input()!=None):
        state['slider_value'] = get_user_input()

    return state