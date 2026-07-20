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

# Function for encrypting the text
def encryption():
    # Get the passcode entered by user
    secret_key = passcode.get()

    # Check is password is correct
    if secret_key == "CSI3480":
        # The text entered by user
        msg = first_text.get(1.0, END)

        # Check is message is empty
        if len(msg.strip()) == 0:
            # If message is empty, display error message
            messagebox.showerror("ERROR", "Please enter a text to encrypt.")
        else:
            # Encryption screen
            encrypt_screen = Toplevel(machine_screen)
            encrypt_screen.title("Encrypted Text")
            encrypt_screen.geometry("250x200")
            encrypt_screen.configure(bg="lightgreen")

            # Favicon
            favicon = PhotoImage(file="favicon.png")
            encrypt_screen.iconphoto(False, favicon)

            # Encrypt the text entered by user
            encoded_msg = msg.encode("ascii")
            bytes = base64.b64encode(encoded_msg)
            encrypted_text = bytes.decode("ascii")

            # Display encrypted text on the screen
            Label(encrypt_screen, text="Encrypted Text:", font=("calibri", 13), fg="black", bg="lightgreen").place(x=20, y=20)
            encrypted_output = Text(encrypt_screen, font=("calibri", 13), bg="white", relief=GROOVE, wrap=WORD, bd=0)
            encrypted_output.place(x=25, y=55, width=170, height=75)
            encrypted_output.insert(END, encrypted_text)
            encrypted_output.configure(state=DISABLED)  # Read-Only

            # Scrollbar for encypted textbox
            en_scrollbar = Scrollbar(encrypted_output, orient=VERTICAL, command=encrypted_output.yview)
            encrypted_output.configure(yscrollcommand=en_scrollbar.set)
            en_scrollbar.pack(side=RIGHT, fill=Y)


    # Warning messages for empty or incorrect password
    elif secret_key == "":
        messagebox.showerror("ERROR", "Please input a password to continue.")

    elif secret_key != "CSI3480":
        messagebox.showerror("ERROR", "Incorrect Password. Please try again.")

# Function for decrypting the text
def decryption():
    # Get the passcode entered by user
    secret_key = passcode.get()

    # Check is password is correct
    if secret_key == "CSI3480":
        # The text entered by user
        msg = first_text.get(1.0, END)
        
        # Check whether the message is empty or not a multiple of 4
        if len(msg.strip()) % 4 != 0:
            # If message is not a multiple of 4, display error message
            messagebox.showerror("ERROR", "Invalid input. Please enter a valid encrypted text.")
        elif len(msg.strip()) == 0:
            # If message is empty, display error message
            messagebox.showerror("ERROR", "Please enter a text to decrypt.")
        else:
            # Decryption screen
            decrypt_screen = Toplevel(machine_screen)
            decrypt_screen.title("Decrypted Text")
            decrypt_screen.geometry("250x200")
            decrypt_screen.configure(bg="lightblue")

            # Favicon
            favicon = PhotoImage(file="favicon.png")
            decrypt_screen.iconphoto(False, favicon)

            # Decrypt the text entered by user
            decoded_msg = msg.encode("ascii")
            bytes = base64.b64decode(decoded_msg)
            decrypted_text = bytes.decode("ascii")

            # Display decrypted text on the screen
            Label(decrypt_screen, text="Decrypted Text:", font=("calibri", 13), fg="black", bg="lightblue").place(x=20, y=20)
            decrypted_output = Text(decrypt_screen, font=("calibri", 13), bg="white", relief=GROOVE, wrap=WORD, bd=0)
            decrypted_output.place(x=25, y=55, width=170, height=75)
            decrypted_output.insert(END, decrypted_text)
            decrypted_output.configure(state=DISABLED) # Read-Only

            # Scrollbar for decrypted textbox
            de_scrollbar = Scrollbar(decrypted_output, orient=VERTICAL, command=decrypted_output.yview)
            decrypted_output.configure(yscrollcommand=de_scrollbar.set)
            de_scrollbar.pack(side=RIGHT, fill=Y)

    # Warning messages for empty or incorrect password
    elif secret_key == "":
        messagebox.showerror("ERROR", "Please input a password to continue.")

    elif secret_key != "CSI3480":
        messagebox.showerror("ERROR", "Incorrect Password. Please try again.")

# Main GUI Screen for Cipher Machine Tool
def machine_screen():
    # Global variables to use across all functions
    global machine_screen, passcode, first_text

    # Main window screen title and size (using Tkinter)
    machine_screen = Tk()
    machine_screen.geometry("387x355")
    machine_screen.title("Cipher Machine")
    
    # Favicon
    favicon = PhotoImage(file="favicon.png")
    machine_screen.iconphoto(False, favicon)
    
    # Function to reset the text and passcode fields
    def reset_machine():
        passcode.set("")
        first_text.delete(1.0, END)

    # Textbox for user input
    Label(text="Enter Text:", fg="black", font=("calibri", 13)).place(x=20, y=20)
    first_text = Text(highlightthickness=1, font=("calibri", 13), bg="white", relief=GROOVE, wrap=WORD, bd=0)
    first_text.place(x=20, y=50, width=351, height=75)
    
    # Scrollbar for the textbox
    scrollbar = Scrollbar(first_text, orient=VERTICAL, command=first_text.yview)
    first_text.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Textbox for password input
    Label(text="Enter Passcode:", fg="black", font=("calibri", 13)).place(x=20, y=150)
    passcode = StringVar()
    Entry(textvariable=passcode, width=38, highlightthickness=1, font=("calibri", 13), show="*").place(x=20, y=180)

    # Encrypt, Decrypt, and Reset buttons
    Button(text="Encrypt", height=2, width=22, bg="lightgreen", fg="black", bd=0, command=encryption).place(x=20, y=230)
    Button(text="Decrypt", height=2, width=22, bg="lightblue", fg="black", bd=0, command=decryption).place(x=206, y=230)
    Button(text="Reset", height=2, width=48, bg="lightcoral", fg="black", bd=0, command=reset_machine).place(x=22, y=275)

    # Run the application
    machine_screen.mainloop()

# Display screen function when run is clicked
machine_screen()