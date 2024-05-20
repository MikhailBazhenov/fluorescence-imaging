# This program records left mouse button clicks and keyboard input
import ctypes
import time
import pynput

print('This program records left mouse button clicks and keyboard input.')
print('To escape first click right mouse button, and then ESC key.')
timer = []
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
begin_time = time.time()


def on_click(x, y, button, pressed):
    global begin_time
    # Check if the left button was pressed
    if pressed and button == pynput.mouse.Button.left:
        # Print the click coordinates
        print(x, y)
        timer.append([0, x, y, time.time() - begin_time])
        begin_time = time.time()
    if pressed and button == pynput.mouse.Button.right:
        return False


def on_press(key):
    global begin_time
    try:
        print(key.char)
        timer.append([1, key.char, '_', time.time() - begin_time])
        begin_time = time.time()
    except AttributeError:
        print('special key {0} pressed'.format(key))
        timer.append([2, key, '_', time.time() - begin_time])
        begin_time = time.time()


def on_release(key):
    # print('{0} released'.format(key))
    if key == pynput.keyboard.Key.esc:
        # Stop listener
        return False


mouse_listener = pynput.mouse.Listener(on_click=on_click)
key_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener.start()
key_listener.start()
mouse_listener.join()
key_listener.join()

f1 = open('mouse+keys.txt', 'w')
for t in timer:
    f1.write(str(t[0]) + '\t' + str(t[1]) + '\t' + str(t[2]) + '\t' + str(t[3]) + '\n')



