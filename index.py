from tkinter import *
from tkinter import messagebox
import base64
import os

def screen():
    # Main GUI Screen for Cipher Machine Tool
    screen = Tk()
    screen.geometry("400x400")
    
    # Favicon
    favicon = PhotoImage(file="favicon.png")
    screen.iconphoto(False, favicon)

    screen.title("Cipher Machine")
    screen.mainloop()
screen()

