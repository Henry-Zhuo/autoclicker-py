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
# is between 0 seconds and soon after AUTOCLICK_CLICK_TIME seconds has passed 
AUTOCLICK_CLICK_TIME = 1
AUTOCLICK_CLICKS_PER_SECOND = 21
# Time in seconds between clicks for autoclicker
AUTOCLICK_CLICK_INTERVAL = 1 / AUTOCLICK_CLICKS_PER_SECOND
AUTOCLICK_COUNT = int(AUTOCLICK_CLICK_TIME / AUTOCLICK_CLICK_INTERVAL)
AUTOCLICK_HOTKEY = '1'
HOTKEY_START_SEQUENCE = 'f7'
ESCAPE_MACRO_START_SEQUENCE = 'esc'

idle_autoclick_thread = None
running_autoclick_thread = multiprocessing.Process()



def __autoclick():
    while True:
        pyautogui.click(clicks=AUTOCLICK_COUNT, interval=AUTOCLICK_CLICK_INTERVAL)



def toggle_autoclicker():
    global idle_autoclick_thread
    global running_autoclick_thread

    if running_autoclick_thread.is_alive():
        running_autoclick_thread.kill()
        # Should close() process but crashes right after kill and takes time
    else:
        idle_autoclick_thread.start()
        running_autoclick_thread = idle_autoclick_thread
        idle_autoclick_thread = multiprocessing.Process(target=__autoclick)



def main():
    global idle_autoclick_thread
    global running_autoclick_thread
    idle_autoclick_thread = multiprocessing.Process(target=__autoclick)

    keyboard.add_hotkey(f"{HOTKEY_START_SEQUENCE}+{AUTOCLICK_HOTKEY}", toggle_autoclicker, suppress=True)

    keyboard.add_hotkey(f'{ESCAPE_MACRO_START_SEQUENCE}+{HOTKEY_START_SEQUENCE}', lambda: keyboard.write(HOTKEY_START_SEQUENCE))
    while True:
        keyboard.wait(HOTKEY_START_SEQUENCE, suppress=True)



if __name__ == '__main__':
    main()
