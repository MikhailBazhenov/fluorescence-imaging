# This program allows automation of imaging using MUSES9-HS software on Windows PC.
# It makes this by performing mouse-clicking and keyboard-input scripts.
# Most probably, it will not work on your PC at first.
# Please read all comments carefully and make the changes necessary.
# At the first start, the program will try to install all the libraries needed.

import os
import sys
import subprocess
import time


def install(package):
    positive_responses = ['Y', 'y']
    print('The package <' + package + '> is not installed on your PC.')
    response = input('Do you want to install it now? (Y/N): ')
    if response in positive_responses:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print('Sorry, the program will not work without it.')
        time.sleep(5)
        exit()

try:
    import ctypes
except:
    install('ctypes')
    import ctypes

try:
    import numpy as np
except:
    install('numpy')
    import numpy as np

try:
    import pynput
    from pynput.keyboard import Key
except:
    install('pynput')
    import pynput
    from pynput.keyboard import Key

try:
    from PIL import ImageGrab
except:
    install('pillow')
    from PIL import ImageGrab

try:
    import win32gui
except:
    install('win32gui')
    import win32gui

# Two lines below are needed to position a window of a program not to interfere
# with lunching Muses9-HS application from the desktop by mouse clicking.
# Here you should input the correct path to py.exe on your PC ↓↓↓
try:
    hwnd = win32gui.FindWindow(None, r'C:\Users\SpectriconDevPC\AppData\Local\Programs\Python\Launcher\py.exe')
    win32gui.MoveWindow(hwnd, 300, 300, 600, 300, True)
except:
    print('Please, check the program <mouse_player.py> on line 60.')


def screenshot():  # This program makes screenshots to know if something went wrong with Muses9-HS app
    snapshot = ImageGrab.grab()
    dif = abs(np.sum(np.subtract(snapshot, first_snapshot)))
    if dif > 1000:
        print('Error found! Restarting in 5 seconds!')
        time.sleep(5)
        os.system('shutdown -t 0 -r -f')  # If something went wrong it restarts the PC
        # For this to work correctly, you should make this program
        # to run automatically on OS start through Windows task manager
        # and ensure the user to login automatically (without password)
    else:
        return()


p = 'C:\\Users\\SpectriconDevPC\\Desktop\\mouse_click\\'  # This is the path to settings file
f4 = open(p + 'settings.txt', 'r')
end_time_txt = f4.readline().strip()  # Settings file contains the date and time when to stop the program
interval_txt = f4.readline().strip()  # and the interval between loop cycles in seconds.
interval = int(interval_txt)
end_time = time.mktime(time.strptime(end_time_txt, '%d-%m-%Y %H:%M:%S'))

if end_time > time.time():
    print('We will proceed in 5 seconds.')
    time.sleep(5)
else:
    print('End time passed. Change settings.txt')
    time.sleep(5)
    exit()

timer1 = []
timer2 = []
timer3 = []
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

# Reading the script, that executes only once at the beginning
f1 = open(p + 'mouse_begin.txt', 'r')
for t in f1:
    click = t.strip().split()
    z = int(click[0])
    if z == 0:
        x = int(click[1])
        y = int(click[2])
    if z == 1:
        x = click[1]
        y = click[2]
    if z == 2:
        if click[1] == 'Key.space':
            x = Key.space
        if click[1] == 'Key.shift':
            x = Key.shift
        if click[1] == 'Key.backspace':
            x = Key.backspace
        if click[1] == 'Key.esc':
            x = Key.esc
        y = click[2]
    wait = float(click[3])
    timer1.append([z, x, y, wait])

# Reading the loop script that will be executed continuously
# with an interval in between cycles indicated in the <settings.txt> file.
f2 = open(p + 'mouse_loop.txt', 'r')
for t in f2:
    click = t.strip().split()
    z = int(click[0])
    if z == 0:
        x = int(click[1])
        y = int(click[2])
    if z == 1:
        x = click[1]
        y = click[2]
    if z == 2:
        if click[1] == 'Key.space':
            x = Key.space
        if click[1] == 'Key.shift':
            x = Key.shift
        if click[1] == 'Key.backspace':
            x = Key.backspace
        if click[1] == 'Key.esc':
            x = Key.esc
        y = click[2]
    wait = float(click[3])
    timer2.append([z, x, y, wait])

# Reading the end script that will be executed once at the end.
f3 = open(p + 'mouse_end.txt', 'r')
for t in f3:
    click = t.strip().split()
    z = int(click[0])
    if z == 0:
        x = int(click[1])
        y = int(click[2])
    if z == 1:
        x = click[1]
        y = click[2]
    if z == 2:
        if click[1] == 'Key.space':
            x = Key.space
        if click[1] == 'Key.shift':
            x = Key.shift
        if click[1] == 'Key.backspace':
            x = Key.backspace
        if click[1] == 'Key.esc':
            x = Key.esc
        y = click[2]
    wait = float(click[3])
    timer3.append([z, x, y, wait])

# Now we perform all the scripts.
# begin
for t in timer1:
    if t[0] == 0:
        time.sleep(t[3])
        mouse.position = (t[1], t[2])
        if t[3] < 1:
            mouse.click(pynput.mouse.Button.left, 2)
        else:
            mouse.click(pynput.mouse.Button.left, 1)
        print(t[1], t[2])
    if t[0] == 1:
        if t[1] == 'file':
            keyboard.type('image_' + time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime()))
        else:
            keyboard.type(t[1])
        print(t[1])
    if t[0] == 2:
        keyboard.press(t[1])
        keyboard.release(t[1])
    if t[0] == 3:
        first_snapshot = ImageGrab.grab()
time.sleep(interval)

# loop
while True:
    if time.time() > end_time:
        break
    for t in timer2:
        if t[0] == 0:
            time.sleep(t[3])
            mouse.position = (t[1], t[2])
            if t[3] < 1:
                mouse.click(pynput.mouse.Button.left, 2)
            else:
                mouse.click(pynput.mouse.Button.left, 1)
            print(t[1], t[2])
        if t[0] == 1:
            if t[1] == 'file':
                keyboard.type('image_'+time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime()))
            else:
                keyboard.type(t[1])
            print(t[1])
        if t[0] == 2:
            keyboard.press(t[1])
            keyboard.release(t[1])
        if t[0] == 3:
            screenshot()
    time.sleep(interval)


# end
for t in timer3:
    if t[0] == 0:
        time.sleep(t[3])
        mouse.position = (t[1], t[2])
        if t[3] < 1:
            mouse.click(pynput.mouse.Button.left, 2)
        else:
            mouse.click(pynput.mouse.Button.left, 1)
        print(t[1], t[2])
    if t[0] == 1:
        if t[1] == 'file':
            keyboard.type('image_' + time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime()))
        else:
            keyboard.type(t[1])
        print(t[1])
    if t[0] == 2:
        keyboard.press(t[1])
        keyboard.release(t[1])
    if t[0] == 3:
        screenshot()
