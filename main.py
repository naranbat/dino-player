import sys
import random 
from time import sleep
import pygetwindow as gw
import pyautogui as ag 
from mss import mss 
import numpy as np
import cv2
from time import time
import ctypes


ag.PAUSE = .5
ag.FAILSAFE = True
game_window = object()


def open_chrome():
    ag.hotkey('win','r')
    ag.typewrite('chrome')
    ag.press('enter')
    ag.typewrite('chrome://dino')
    ag.press('enter')
    run_chrome()


def setup_window(window):
    window.resizeTo(800, 600)
    window.moveTo(-10, 0)


def activate_window(window):
    window.activate()


def run_chrome():
    global game_window
    for window in gw.getAllWindows():
        if window.title == 'chrome://dino/ - Google Chrome':
            setup_window(window)
            game_window = window
            return
    open_chrome()


def get_pixel(meta):
    with mss() as sct:
        return cv2.cvtColor(np.array(sct.grab(meta)), cv2.COLOR_BGR2GRAY)


def game_over():
    spot = get_pixel({"mon":0, "top": 298, "left": 383, "width":1, "height": 1})
    bg_spot = get_pixel({"mon":0, "top": 380, "left": 210, "width":1, "height": 1})
    if int(spot[0][0]/100) != int(bg_spot[0][0]/100):
        print('Game Over!')
        return True
    return False


def noob():
    print('[jump]')
    ag.press('space')
    sleep(random.randint(80,100)/100)


def cheat():
    ag.moveTo(250,110)
    ag.click(button='right')
    ag.click(ag.locateOnScreen('./patterns/inspect-menu.png', grayscale=True, confidence=.9))
    ag.click(ag.locateOnScreen('./patterns/console-tab.png', grayscale=True, confidence=.9))
    ag.typewrite('Runner.instance_.gameOver = () => {}') # overwrite gameOver function :)
    ag.press('enter', presses=3)
    ag.click(ag.locateOnScreen('./patterns/close-console.png', grayscale=True, confidence=.9))


def normal():
    obstacle = get_pixel({"mon":0, "top": 320, "left": 200, "width":30, "height": 25})
    if (obstacle != obstacle[0][0]).any():
        print('[jump]')
        ag.press('space')


duck = False
time_interval = 2.95
add_distance_time = time()+time_interval
view_distance = 60

def pro():
    global duck
    global view_distance
    global add_distance_time

    obstacle = get_pixel({"mon":0, "top": 350, "left": 190, "width":view_distance, "height": 1})
    if (obstacle != obstacle[0][0]).any():
        print('[jump]')
        ag.press('space')
        duck = True

    ground_x = get_pixel({"mon":0, "top": 332, "left": 100, "width":250, "height": 1})
    if duck and (ground_x == ground_x[0][0]).all():
        duck = False
        print('[duck]')
        ag.keyDown('down')
        sleep(0.05)
        ag.keyUp('down')

    if view_distance < 300 and add_distance_time < time():
        view_distance += 1
        add_distance_time = time() + time_interval 
        print('[x]')



def play(mode):
    ag.PAUSE = .5
    run_chrome()
    activate_window(game_window)

    if mode == 'immortal':
        cheat()
        mode = 'noob' # overwrite mode

    ag.press('space')
    ag.PAUSE = 0.1
    while True:
        if game_over():
            break
        globals()[mode]()


def main(mode):
    mode = mode.strip().lower()
    if mode in ['noob','immortal','normal','pro']:
        play(mode)
    else:
        help()


def help():
    print("""python main.py [mode]
    noob\tHopeless
    immortal\tImmortal Dino
    normal\tMe ;D 
    pro\t\tPro player
    """)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            main(sys.argv[1])
        except KeyboardInterrupt:
            print("Stopped!")
    else:
        help()