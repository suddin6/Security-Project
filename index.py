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

# Variables to store passwords
create_pw = ""
change_pw = ""
old_pw = ""

# Encrypt and Decrypt screens
encrypt_screen = ""
decrypt_screen = ""

# Function to copy encrypted text
def copy_encrypt():
    # Global variables
    global e_copy_toggle, encrypt_screen, encrypted_text

    # If copy in encryption clicked, show success message
    if e_copy_toggle == True:
        messagebox.showinfo("SUCCESS", "Text has been copied successfully!")
    
    # Copy the text and update screen
    encrypt_screen.clipboard_clear()
    encrypt_screen.clipboard_append(
        encrypted_text.strip()
    )
    encrypt_screen.update()

# Function for encrypting the text
def encryption():
    # Global variables
    global encrypted_text, mode, encrypt_screen, e_copy_toggle

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
            encrypt_screen.resizable(0,0)
            encrypt_screen.configure(bg="plum")

            # Favicon
            favicon = PhotoImage(file="favicon.png")
            encrypt_screen.iconphoto(False, favicon)

            # Encrypt the text entered by user
            encoded_msg = msg.encode("ascii")
            bytes = base64.b64encode(encoded_msg)
            encrypted_text = bytes.decode("ascii")

            # Display encrypted text on the screen
            Label(encrypt_screen, text="Encrypted Text:", font=("calibri", 13), fg="black", bg="plum").place(x=20, y=20)
            encrypted_output = Text(encrypt_screen, font=("calibri", 13), bg="white", relief=GROOVE, wrap=WORD, bd=0)
            encrypted_output.place(x=25, y=55, width=200, height=75)
            encrypted_output.delete(1.0, END)
            encrypted_output.insert(END, encrypted_text)
            encrypted_output.configure(state=DISABLED)  # Read-Only

            # Scrollbar for encypted textbox
            en_scrollbar = Scrollbar(encrypted_output, orient=VERTICAL, command=encrypted_output.yview)
            encrypted_output.configure(yscrollcommand=en_scrollbar.set)
            en_scrollbar.pack(side=RIGHT, fill=Y)

            # Check whether copy button was clicked
            e_copy_toggle = True

            # Button to copy encrypted text
            Button(encrypt_screen, text="Copy", command=copy_encrypt, bg="blue", fg="white", height=1, width=12).place(x=20, y=150)
    # Warning messages for empty or incorrect password
    elif secret_key == "":
        messagebox.showerror("ERROR", "Please input a password to continue.")
    elif secret_key != create_pw:
        messagebox.showerror("ERROR", "Incorrect Password. Please try again.")

# Function to copy decrypted text
def copy_decrypt():
    # Global variables
    global copy_toggle, decrypt_screen, decrypted_output

    # If copy in decryption clicked, show success message
    if copy_toggle == True:
        messagebox.showinfo("SUCCESS", "Text has been copied successfully!")

    # Copy the text and update screen
    decrypt_screen.clipboard_clear()
    decrypt_screen.clipboard_append(
        decrypted_text.strip()
    )
    decrypt_screen.update()

# Function for decrypting the text
def decryption():
    # Global variables
    global decrypted_text, mode, decrypt_screen, copy_toggle

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
            decrypt_screen.resizable(0,0)
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
            decrypted_output.place(x=25, y=55, width=200, height=75)
            decrypted_output.delete(1.0, END)
            decrypted_output.insert(END, decrypted_text)
            decrypted_output.configure(state=DISABLED) # Read-Only

            # Scrollbar for decrypted textbox
            de_scrollbar = Scrollbar(decrypted_output, orient=VERTICAL, command=decrypted_output.yview)
            decrypted_output.configure(yscrollcommand=de_scrollbar.set)
            de_scrollbar.pack(side=RIGHT, fill=Y)

            # Check whether copy button was clicked
            copy_toggle = True

            # Button to copy decrypted text
            Button(decrypt_screen, text="Copy", command=copy_decrypt, bg="blue", fg="white", height=1, width=12).place(x=20, y=150)
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

# Function to track the password
def save_password():
    # Global variables
    global create_pw, old_pw, change_pw

    try:
        # Execute this code if file does not exist or is empty
        if not os.path.exists("passwords.txt") or os.path.getsize("passwords.txt") == 0:
            # Ask user to create password
            create_pw = simpledialog.askstring("PASSWORD", "Please create a password to continue:")
            # No empty submissions
            if create_pw == "":
                messagebox.showinfo("ERROR", "Please do not leave the field blank.")
            # Write and save password to text file
            with open("passwords.txt", "w") as file:
                file.write(create_pw)
            messagebox.showinfo("SUCCESS", "Password has been saved.")
        else:
            # Read password from file
            with open("passwords.txt", "r") as file:
                create_pw = file.read().strip()
    # Display an errors
    except Exception as error:
        messagebox.showerror("ERROR", f"An error occurred: {str(error)}")

# Function to change passwords
def change_password():
    # Global variables
    global create_pw, old_pw, change_pw

    try:
        # Only allow changing if file exists
        if os.path.exists("passwords.txt"):
            change_pw = messagebox.askyesno("PASSWORD", "Would you like to change your password?")
            if change_pw == True:
                old_pw = simpledialog.askstring("OLD PASSWORD", "Please enter your old password: ")
                if old_pw is None:
                    return
                # Check if old password is known by user
                if old_pw == create_pw:
                    new_pw = simpledialog.askstring("NEW PASSWORD", "Please enter your new password: ")
                    if new_pw is None:
                        return
                    elif new_pw == "":
                        messagebox.showinfo("ERROR", "Please do not leave the field blank.")
                        return
                    # Write new password into file and override old one
                    with open("passwords.txt", "w") as file:
                        create_pw = new_pw
                        file.write(create_pw)
                    messagebox.showinfo("SUCCESS", "Password has been saved.")
                elif old_pw != create_pw:
                    messagebox.showinfo("ERROR", "Your password is incorrect. Please try again")
    # Display errors to user
    except Exception as error:
        messagebox.showerror("ERROR", f"An error occurred: {str(error)}")


# Main GUI Screen for Cipher Machine Tool
def machine_screen():
    # Global variables to use across all functions
    global machine_screen, passcode, first_text

    # Call the save_password function to allow a user to create a password
    save_password()

    # Main window screen title and size (using Tkinter)
    machine_screen = Tk()
    machine_screen.geometry("387x387")
    machine_screen.resizable(0,0)
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

    # Change Password, Encrypt, Decrypt, Reset, and Save buttons
    Button(text="Change Password", height=1, width=13, bg="beige", fg="black", bd=0, command=change_password).place(x=270, y=210)
    Button(text="Encrypt", height=2, width=22, bg="plum", fg="black", bd=0, command=encryption).place(x=20, y=240)
    Button(text="Decrypt", height=2, width=22, bg="lightblue", fg="black", bd=0, command=decryption).place(x=206, y=240)
    Button(text="Reset", height=2, width=48, bg="lightcoral", fg="black", bd=0, command=reset_machine).place(x=22, y=285)
    Button(text="Save", height=2, width=48, bg="DarkOliveGreen1", fg="black", bd=0, command=save_text).place(x=22, y=330)

    # Run the application
    machine_screen.mainloop()
# Display screen function when run is clicked
machine_screen()