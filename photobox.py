from gpiozero import Button
import time
import os
import datetime


def wait_for_button():
    button = Button(12)
    is_button_pressed = button.is_pressed()
    while is_button_pressed:
        is_button_pressed = is_button_pressed()
    # end
# end


def set_background(filename):
    os.system("pcmanfm --set-wallpaper " + filename)
# end


def take_picture_and_set_background():
    ts = time.time()
    filename = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S') + ".jpg"
    take_picture(filename)
    set_background(fielename)
# end


def take_picture(filename):
    os.system("raspistill -o " + filename + " -t 3000 -f")
# end


def main_program():
    while True:
        wait_for_button()
        take_picture_and_set_background()
    # end


main_program()

