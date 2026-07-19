'''
Sumaya Uddin and Emma Hochron
Group J - Cipher Machine [Project Implementation]
Professor Solmaz Salehian
CSI 3480 - Security and Privacy in Computing
Due: August 13, 2026
Description: An encryption-decryption tool that utilizes a GUI interface and allows for secure messaging!
'''

from tkinter import *
from tkinter import messagebox
import base64
import os

# Main GUI Screen for Cipher Machine Tool
def screen():
    screen = Tk()
    screen.geometry("400x400")
    
    # Favicon
    favicon = PhotoImage(file="favicon.png")
    screen.iconphoto(False, favicon)

    screen.title("Cipher Machine")
    
    # Textbox for user input
    Label(text="Enter Text:", fg="black", font=("calibri", 13)).place(x=20, y=20)
    first_text = Text(font=("calibri", 13), bg="white", relief=GROOVE, wrap=WORD, bd=0)
    first_text.place(x=20, y=50, width=355, height=100)

    # Textbox for password input
    Label(text="Enter Passcode:", fg="black", font=("calibri", 13)).place(x=20, y=160)
    passcode = StringVar()
    Entry(textvariable=passcode, width=19, bd=0, font=("calibri", 13), show="*").place(x=20, y=190)

    screen.mainloop()
screen()

