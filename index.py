'''
Sumaya Uddin and Emma Hochron
Group J - Cipher Machine [Project Implementation]
Professor Solmaz Salehian
CSI 3480 - Security and Privacy in Computing
Due: August 13, 2026
Description: An encryption-decryption tool that utilizes a GUI interface and allows for secure messaging!
'''

# Importing from tkinter library (GUI), base64 (encryption + decryption), os (file handling)
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
import base64
import os
import tkinter.font as tkfont


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

# Color scheme
main_bg = "#16241C"
main_text = "#AAD1B6"
textbox_bg = "#000000"
btn_color1 = "#425A4F"
btn_color2 = "#5E5577"
btn_color3 = "#815B5B"
btn_color4 = "#5B6F81"
btn_color5 = "#7D815B"
btn_color6 = "#2C332E"
scrollbar_color = "#2C332E"
scrollbar_color2 = "black"
scrollbar_color3 = "#8DB699"


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
    global encrypted_text, mode, encrypt_screen, e_copy_toggle

    mode = "encrypt"
    secret_key = passcode.get()

    if secret_key == create_pw:
        msg = first_text.get(1.0, END)

        if len(msg.strip()) == 0:
            messagebox.showerror("ERROR", "Please enter a text to encrypt.")
        else:
            encrypt_screen = Toplevel(machine_screen)
            encrypt_screen.title("Encrypted Text")
            encrypt_screen.geometry("280x220")
            encrypt_screen.minsize(220, 180)
            encrypt_screen.configure(bg="plum")

            favicon = PhotoImage(file="favicon.png")
            encrypt_screen.iconphoto(False, favicon)

            encrypt_screen.columnconfigure(0, weight=1)
            encrypt_screen.rowconfigure(1, weight=1)

            encoded_msg = msg.encode("utf-8")
            bytes = base64.b64encode(encoded_msg)
            encrypted_text = bytes.decode("utf-8")

            Label(encrypt_screen, text="Encrypted Text:", font=fixed_font, fg="black", bg="plum").grid(
                row=0, column=0, sticky="w", padx=15, pady=(15, 0)
            )

            # Row 1: text box + scrollbar, in their own frame
            output_frame = Frame(encrypt_screen)
            output_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
            output_frame.columnconfigure(0, weight=1)
            output_frame.rowconfigure(0, weight=1)

            encrypted_output = Text(output_frame, font=fixed_font, bg="white", relief=FLAT, wrap=WORD, bd=0)
            encrypted_output.grid(row=0, column=0, sticky="nsew")
            encrypted_output.delete(1.0, END)
            encrypted_output.insert(END, encrypted_text)
            encrypted_output.configure(state=DISABLED)

            en_scrollbar = Scrollbar(output_frame, orient=VERTICAL, command=encrypted_output.yview)
            en_scrollbar.grid(row=0, column=1, sticky="ns")
            encrypted_output.configure(yscrollcommand=en_scrollbar.set)

            e_copy_toggle = True

            Button(encrypt_screen, text="Copy", command=copy_encrypt, bg="blue", fg="white", font=btn_fixed_font).grid(
                row=2, column=0, sticky="w", padx=15, pady=(5, 15)
            )
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
    global decrypted_text, mode, decrypt_screen, copy_toggle

    mode = "decrypt"
    secret_key = passcode.get()

    if secret_key == create_pw:
        msg = first_text.get(1.0, END)

        if len(msg.strip()) % 4 != 0:
            messagebox.showerror("ERROR", "Invalid input. Please enter a valid encrypted text.")
        elif len(msg.strip()) == 0:
            messagebox.showerror("ERROR", "Please enter a text to decrypt.")
        else:
            decrypt_screen = Toplevel(machine_screen)
            decrypt_screen.title("Decrypted Text")
            decrypt_screen.geometry("280x220")
            decrypt_screen.minsize(220, 180)
            decrypt_screen.configure(bg="lightblue")

            favicon = PhotoImage(file="favicon.png")
            decrypt_screen.iconphoto(False, favicon)

            decrypt_screen.columnconfigure(0, weight=1)
            decrypt_screen.rowconfigure(1, weight=1)

            decoded_msg = msg.encode("utf-8")
            bytes = base64.b64decode(decoded_msg)
            decrypted_text = bytes.decode("utf-8")

            Label(decrypt_screen, text="Decrypted Text:", font=fixed_font, fg="black", bg="lightblue").grid(
                row=0, column=0, sticky="w", padx=15, pady=(15, 0)
            )

            # Row 1: text box + scrollbar, in their own frame
            output_frame = Frame(decrypt_screen)
            output_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
            output_frame.columnconfigure(0, weight=1)
            output_frame.rowconfigure(0, weight=1)

            decrypted_output = Text(output_frame, font=fixed_font, bg="white", relief=FLAT, wrap=WORD, bd=0)
            decrypted_output.grid(row=0, column=0, sticky="nsew")
            decrypted_output.delete(1.0, END)
            decrypted_output.insert(END, decrypted_text)
            decrypted_output.configure(state=DISABLED)

            de_scrollbar = Scrollbar(output_frame, orient=VERTICAL, command=decrypted_output.yview)
            de_scrollbar.grid(row=0, column=1, sticky="ns")
            decrypted_output.configure(yscrollcommand=de_scrollbar.set)


            copy_toggle = True

            Button(decrypt_screen, text="Copy", command=copy_decrypt, bg="blue", fg="white", font=btn_fixed_font).grid(
                row=2, column=0, sticky="w", padx=15, pady=(5, 15)
            )
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

# Function to import a file
def import_file():
    # Global variables
    global first_text

    # Retreiving text file from user
    path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
    
    # If the path exists/is correct, read the contents and put it in the textbox
    if path:
        with open(path, "r") as file:
            first_text.delete(1.0, END)
            file_contents = file.read().strip()
            first_text.insert(END, file_contents)
        # Display success message
        messagebox.showinfo("SUCCESS", "You have successfully imported a file!")

# Main GUI Screen for Cipher Machine Tool
def machine_screen():
    global machine_screen, passcode, first_text, fixed_font, btn_fixed_font

    save_password()

    machine_screen = Tk()
    machine_screen.geometry("400x420")
    machine_screen.title("Cipher Machine")
    machine_screen.minsize(420, 380)  # minimum window size
    machine_screen.configure(bg=main_bg)

    base_family = tkfont.nametofont("TkFixedFont").actual("family")
    fixed_font = tkfont.Font(family=base_family, size=13)
    btn_fixed_font = tkfont.Font(family=base_family, size=9)


    #Scrollbar styling
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Custom.Vertical.TScrollbar",
        background=scrollbar_color,      # thumb color
        troughcolor=scrollbar_color2,     # track color
        bordercolor=scrollbar_color2,
        arrowcolor=scrollbar_color3,
        lightcolor=scrollbar_color,
        darkcolor=scrollbar_color
    )

    style.map(
        "Custom.Vertical.TScrollbar",
        background=[("disabled", scrollbar_color), ("active", scrollbar_color)],
        arrowcolor=[("disabled", scrollbar_color3)]
    )

    favicon = PhotoImage(file="favicon.png")
    machine_screen.iconphoto(False, favicon)

    machine_screen.columnconfigure(0, weight=1)
    machine_screen.columnconfigure(1, weight=1)
    machine_screen.rowconfigure(1, weight=1)  # only the text box row grows vertically

    def reset_machine():
        passcode.set("")
        first_text.delete(1.0, END)

    # Row 0: label
    Label(text="Enter Text:", bg=main_bg, fg=main_text, font=fixed_font).grid(
        row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 0)
    )

    # Row 1: text box + scrollbar, in their own frame
    text_frame = Frame(machine_screen)
    text_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    text_frame.columnconfigure(0, weight=1)
    text_frame.rowconfigure(0, weight=1)

    first_text = Text(text_frame,
        font=fixed_font,
        bg=textbox_bg,
        fg=main_text,
        insertbackground=main_text,
        relief=FLAT,
        wrap=WORD,
        bd=0,
        height=4,
        highlightthickness=1,
        highlightbackground=textbox_bg,
        highlightcolor=textbox_bg
    )
    first_text.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(text_frame, orient=VERTICAL, command=first_text.yview, style="Custom.Vertical.TScrollbar")
    scrollbar.grid(row=0, column=1, sticky="ns")
    first_text.configure(yscrollcommand=scrollbar.set)

    # Row 2: passcode label
    Label(text="Enter Passcode:", bg=main_bg, fg=main_text, font=fixed_font).grid(
        row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 0)
    )

    # Row 3: passcode entry + button
    passcode_frame = Frame(machine_screen, bg=main_bg)
    passcode_frame.grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=5)

    passcode = StringVar()
    Entry_widget = Entry(
        passcode_frame, textvariable=passcode, width=25, font=fixed_font, show="*",
        bg=textbox_bg, fg=main_text, insertbackground=main_text,
        relief=FLAT, bd=0,
        highlightthickness=1,
        highlightbackground=textbox_bg,  # ring color when unfocused
        highlightcolor=textbox_bg        # ring color when focused
    )
    Entry_widget.pack(side=LEFT)
    Button(passcode_frame, text="Change Password", bg=btn_color6, relief=FLAT, fg=main_text, font=btn_fixed_font, activebackground=btn_color6, command=change_password).pack(side=LEFT, padx=(5, 0))

    # Row 4: encrypt/decrypt — fixed height (row weight 0), full width
    Button(text="Encrypt", bg=btn_color1, fg=main_text, bd=0, font=btn_fixed_font, command=encryption).grid(
        row=4, column=0, sticky="ew", padx=(20, 5), pady=10, ipady=15
    )
    Button(text="Decrypt", bg=btn_color2, fg=main_text, bd=0, font=btn_fixed_font, command=decryption).grid(
        row=4, column=1, sticky="ew", padx=(5, 20), pady=10, ipady=15
    )

    # Rows 5-7: reset, save, import — fixed height, pinned to bottom since no weight above them
    Button(text="Reset", bg=btn_color3, fg=main_text, bd=0, font=btn_fixed_font, command=reset_machine).grid(
        row=5, column=0, columnspan=2, sticky="ew", padx=20, pady=5, ipady=10
    )
    Button(text="Save", bg=btn_color4, fg=main_text, bd=0, font=btn_fixed_font, command=save_text).grid(
        row=6, column=0, columnspan=2, sticky="ew", padx=20, pady=5, ipady=10
    )
    Button(text="Import File", bg=btn_color5, fg=main_text, bd=0, font=btn_fixed_font, command=import_file).grid(
        row=7, column=0, columnspan=2, sticky="ew", padx=20, pady=(5, 15)
    )

    machine_screen.mainloop()

# Display screen function when run is clicked
machine_screen()