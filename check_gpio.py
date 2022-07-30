from gpiozero import Button
import time
import os
import datetime

def main_program():
    while True:
	button = Button(12)
	print(button.is_pressed)
    # end

print("Start")
main_program()
