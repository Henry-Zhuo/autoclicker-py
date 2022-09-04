import ctypes
import keyboard
import multiprocessing
import pyautogui
import time

# TODO Consider putting this code in a class to help avoid global variables

# TODO Add support for configuration file ignored by git to allow changes to constants without cluttering commit history. Would need to have default values in case the value is not in the configuration file

# Minimum time in seconds for each loop iteration while autoclicking
# Actual time for each loop iteration is AUTOCLICK_COUNT 
# * (time click() takes including it sleeping for AUTOCLICK_CLICK_INTERVAL seconds)
# because click() waits for AUTOCLICK_CLICK_INTERVAL seconds after each click
# The maximum time isn't straightforward to determine 
# but in practice the time between stopping the autoclicker and it stops autoclicking 
# is soon after AUTOCLICK_CLICK_TIME seconds has passed 
# and depends on AUTOCLICK_CLICK_TIME
AUTOCLICK_CLICK_TIME = 1
AUTOCLICK_CLICKS_PER_SECOND = 15
# Time in seconds between clicks for autoclicker
AUTOCLICK_CLICK_INTERVAL = 1 / AUTOCLICK_CLICKS_PER_SECOND
AUTOCLICK_COUNT = int(AUTOCLICK_CLICK_TIME / AUTOCLICK_CLICK_INTERVAL)

autoclick_enabled = multiprocessing.Value(ctypes.c_bool, False)
autoclick_loop_condition_lock = multiprocessing.Condition()



def __autoclick(autoclick_enabled, autoclick_loop_condition_lock):
    while True:
        # Checking a single variable is probably 
        # faster than acquiring a lock and waiting for it to release
        if autoclick_enabled.value:
            pyautogui.click(clicks=AUTOCLICK_COUNT, interval=AUTOCLICK_CLICK_INTERVAL)
        else:
            # Wait on the lock to release
            autoclick_loop_condition_lock.acquire()
            autoclick_loop_condition_lock.wait()
            autoclick_loop_condition_lock.release()



def toggle_autoclicker():
    global autoclick_enabled
    autoclick_enabled.value = not autoclick_enabled.value

    if autoclick_enabled.value:
        # Unblock the autoclicker
        autoclick_loop_condition_lock.acquire()
        autoclick_loop_condition_lock.notify_all()
        autoclick_loop_condition_lock.release()



def init():
    autoclick_thread = multiprocessing.Process(target=__autoclick, args=(autoclick_enabled, autoclick_loop_condition_lock))
    autoclick_thread.start()
