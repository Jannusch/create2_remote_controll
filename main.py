from tkinter.constants import BOTH
from pycreate2 import Create2
import time
import tkinter as tk



def setup():
    port = "/dev/ttyUSB0"
    bot = Create2(port)

    bot.start()

    bot.safe()
    print('Starting...')

    return bot


def onKeyPress(event):
    if event.char == 'w':
        print(event.char)

        bot.drive_direct(100, 100)
    elif event.char == ' ':
        print(event.char)

        bot.drive_direct(0,0)
    if event.char == 's':
        print(event.char)

        bot.drive_direct(-100, -100)
    if event.char == 'd':
        print(event.char)

        bot.drive_direct(-100, 100)
    if event.char == 'a':
        print(event.char)

        bot.drive_direct(100, -100)
    if event.char == 'c':
        if brush_status:
            print(event.char)
            bot.clean(False)
        else:
            print(event.char)
            bot.clean(True) 


global bot, brush_status
brush_status = False
bot = setup()




root = tk.Tk()
root.bind('<KeyPress>', onKeyPress)
root.mainloop()
