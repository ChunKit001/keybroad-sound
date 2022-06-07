import json
import threading

from pyglet import media
from pynput.keyboard import Key as KeyK, Listener as ListenerK, KeyCode as KeyCodeK
from pynput.mouse import Listener as ListenerM

config = {}
last_type = []
is_close = False


def run_keyboard_listener():
    with ListenerK(on_press=on_press, on_release=on_release) as listenerK:
        listenerK.join()


def run_mouse_listener():
    with ListenerM(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as listenerM:
        listenerM.join()


def on_press(key):
    file_name = 'default'
    try:
        if type(key) == KeyCodeK:
            file_name = config.get(key.char)
            last_type.append(key.char)
        elif type(key) == KeyK:
            file_name = config.get(key.name)
            last_type.append(key.name)
        else:
            last_type.append('default')
    except AttributeError:
        last_type.append('default')
    finally:
        play(file_name)


def play(file_name):
    global file
    try:
        file = media.load("sound\\" + file_name)
    except TypeError:
        file_name = config.get('default')
        file = media.load("sound\\" + file_name)
    finally:
        file.play()
        if len(last_type) > 6:
            del last_type[0]


def on_release(key):
    global is_close
    temp = ''
    for i in last_type:
        if type(i) == str:
            temp += i
    if temp == 'qaz123':
        is_close = True
        return False


def on_click(x, y, button, is_press):
    if is_press:
        file_name = config.get('default')
        play(file_name)
    if is_close:
        return False


def on_scroll(x, y, dx, dy):
    # file_name = config.get('bubble')
    # play(file_name)
    if is_close:
        return False


def on_move(x, y):
    if is_close:
        return False


if __name__ == '__main__':
    f = open('config.json', 'r', encoding="utf-8")
    config = json.load(f)
    f.close()

    keyboard_thread = threading.Thread(target=run_keyboard_listener)
    keyboard_thread.start()
    mouse_thread = threading.Thread(target=run_mouse_listener)
    mouse_thread.start()
