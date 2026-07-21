'''
Sumaya Uddin and Emma Hochron
Group J - Cipher Machine [Project Implementation]
Professor Solmaz Salehian
CSI 3480 - Security and Privacy in Computing
Due: August 13, 2026
Description: An encryption-decryption tool that utilizes a GUI interface and allows for secure messaging!
'''

# Importing from tkinter library (GUI), base64 (encryption + decryption), and os (file handling)
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import base64
import os

# Encrypted and decrypted text outputs 
encrypted_text = ""
decrypted_text = ""

# Function for encrypting the text
def encryption():
    # Global variables
    global encrypted_text, mode

    # Toggle to know which button was clicked
    mode = "encrypt"

    # Get the passcode entered by user
    secret_key = passcode.get()

    # Check if password is correct
    if secret_key == create_pw:
        # The text entered by user
        msg = first_text.get(1.0, END)

        # Check if message is empty
        if len(msg.strip()) == 0:
            # If message is empty, display error message
            messagebox.showerror("ERROR", "Please enter a text to encrypt.")
        else:
            # Encryption screen
            encrypt_screen = Toplevel(machine_screen)
            encrypt_screen.title("Encrypted Text")
            encrypt_screen.geometry("250x200")
            encrypt_screen.configure(bg="plum")

            # Favicon
            favicon = PhotoImage(file="favicon.png")
            encrypt_screen.iconphoto(False, favicon)

            # Encrypt the text entered by user
            encoded_msg = msg.encode("ascii")
            bytes = base64.b64encode(encoded_msg)
            encrypted_text += bytes.decode("ascii")

            # Display encrypted text on the screen
            Label(encrypt_screen, text="Encrypted Text:", font=("calibri", 13), fg="black", bg="plum").place(x=20, y=20)
            encrypted_output = Text(encrypt_screen, font=("calibri", 13), bg="white", relief=GROOVE, wrap=WORD, bd=0)
            encrypted_output.place(x=25, y=55, width=170, height=75)
            encrypted_output.delete(1.0, END)
            encrypted_output.insert(END, encrypted_text)
            encrypted_output.configure(state=DISABLED)  # Read-Only

            # Scrollbar for encypted textbox
            en_scrollbar = Scrollbar(encrypted_output, orient=VERTICAL, command=encrypted_output.yview)
            encrypted_output.configure(yscrollcommand=en_scrollbar.set)
            en_scrollbar.pack(side=RIGHT, fill=Y)
    # Warning messages for empty or incorrect password
    elif secret_key == "":
        messagebox.showerror("ERROR", "Please input a password to continue.")
    elif secret_key != create_pw:
        messagebox.showerror("ERROR", "Incorrect Password. Please try again.")

# Function for decrypting the text
def decryption():
    # Global variables
    global decrypted_text, mode

    # Toggle to know which button was clicked
    mode = "decrypt"

    # Get the passcode entered by user
    secret_key = passcode.get()

    # Check if password is correct
    if secret_key == create_pw:
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
            decrypted_text += bytes.decode("ascii")

            # Display decrypted text on the screen
            Label(decrypt_screen, text="Decrypted Text:", font=("calibri", 13), fg="black", bg="lightblue").place(x=20, y=20)
            decrypted_output = Text(decrypt_screen, font=("calibri", 13), bg="white", relief=GROOVE, wrap=WORD, bd=0)
            decrypted_output.place(x=25, y=55, width=170, height=75)
            decrypted_output.delete(1.0, END)
            decrypted_output.insert(END, decrypted_text)
            decrypted_output.configure(state=DISABLED) # Read-Only

            # Scrollbar for decrypted textbox
            de_scrollbar = Scrollbar(decrypted_output, orient=VERTICAL, command=decrypted_output.yview)
            decrypted_output.configure(yscrollcommand=de_scrollbar.set)
            de_scrollbar.pack(side=RIGHT, fill=Y)
    # Warning messages for empty or incorrect password
    elif secret_key == "":
        messagebox.showerror("ERROR", "Please input a password to continue.")
    elif secret_key != create_pw:
        messagebox.showerror("ERROR", "Incorrect Password. Please try again.")

# Function to save messages to a text file
def save_text():
    try:
        # If file does not exist, create one
        if not os.path.exists("saved_msgs.txt"):
            with open("saved_msgs.txt", "w") as file:
                file.write("Here are your saved messages:\n")
            messagebox.showinfo("SUCCESS", "File has been created! Please click the save button once more!")
        else:
            # If encrypt button was clicked, write the encrypted message to file
            if mode == "encrypt":
                with open("saved_msgs.txt", "a") as file:
                    file.write("Encrypted Text: " + encrypted_text + "\n")
            
            # If decrypt button was clicked, write the decrypted message to file
            elif mode == "decrypt":
                with open("saved_msgs.txt", "a") as file:
                    file.write("Decrypted Text: " + decrypted_text + "\n")
    
            # Show success message to user
            messagebox.showinfo("SUCCESS", "Text saved to file successfully!")

    # Display error if any
    except Exception as error:
        messagebox.showerror("ERROR", f"An error occurred: {str(error)}")

# Main GUI Screen for Cipher Machine Tool
def machine_screen():
    # Global variables to use across all functions
    global machine_screen, passcode, first_text, encrypted_button, decrypted_button, create_pw

    # Allow the user to create their own password
    create_pw = simpledialog.askstring("Password","Please create a password to continue:")

    # Main window screen title and size (using Tkinter)
    machine_screen = Tk()
    machine_screen.geometry("387x375")
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

    # Encrypt, Decrypt, Reset, and Save buttons
    encrypted_button = Button(text="Encrypt", height=2, width=22, bg="plum", fg="black", bd=0, command=encryption).place(x=20, y=230)
    decrypted_button = Button(text="Decrypt", height=2, width=22, bg="lightblue", fg="black", bd=0, command=decryption).place(x=206, y=230)
    Button(text="Reset", height=2, width=48, bg="lightcoral", fg="black", bd=0, command=reset_machine).place(x=22, y=275)
    Button(text="Save", height=2, width=48, bg="DarkOliveGreen1", fg="black", bd=0, command=save_text).place(x=22, y=320)

    # Run the application
    machine_screen.mainloop()
# Display screen function when run is clicked
machine_screen()