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
    # Main window screen title and size (using Tkinter)
    screen = Tk()
    screen.geometry("400x400")
    screen.title("Cipher Machine")
    
    # Favicon
    favicon = PhotoImage(file="favicon.png")
    screen.iconphoto(False, favicon)
    
    # Textbox for user input
    Label(text="Enter Text:", fg="black", font=("calibri", 13)).place(x=20, y=20)
    first_text = Text(highlightthickness=1, font=("calibri", 13), bg="white", relief=GROOVE, wrap=WORD, bd=0)
    first_text.place(x=20, y=50, width=355, height=75)
    
    # Scrollbar for the textbox
    scrollbar = Scrollbar(first_text, orient=VERTICAL, command=first_text.yview)
    first_text.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Textbox for password input
    Label(text="Enter Passcode:", fg="black", font=("calibri", 13)).place(x=20, y=150)
    passcode = StringVar()
    Entry(textvariable=passcode, width=38, highlightthickness=1, font=("calibri", 13), show="*").place(x=20, y=180)

    # Run the application
    screen.mainloop()
# Display screen function when run is clicked
screen()

