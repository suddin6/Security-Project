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

first_text = None
second_text = None
action_btn = None

# Variables to store passwords
create_pw = ""
change_pw = ""
old_pw = ""

# Encrypt and Decrypt screens
encrypt_screen = ""
decrypt_screen = ""

# Color scheme (main)
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

#Color scheme (encryption)
en_main_bg = "#241617"
en_textbox_bg = "#000000"
en_btn_color1 = "#5A4D4D"
en_main_text = "#D4C5C5"

#Color scheme (decryption)
de_main_bg = "#161624"
de_textbox_bg = "#000000"
de_btn_color1 = "#4D4F5A"
de_main_text = "#C5C5D4"

mode = "encrypt"  # global toggle state

def perform_action():
    global encrypted_text, decrypted_text, mode, first_text, second_text

    secret_key = passcode.get()

    if secret_key == "":
        show_error("Please input a password to continue.")
        return
    if secret_key != create_pw:
        show_error("Incorrect Password. Please try again.")
        return

    msg = first_text.get(1.0, END)

    if len(msg.strip()) == 0:
        show_error(f"Please enter a text to {mode}.")
        return

    if mode == "encrypt":
        encoded_msg = msg.strip().encode("utf-8")
        encrypted_text = base64.b64encode(encoded_msg).decode("utf-8")
        second_text.configure(state=NORMAL)
        second_text.delete(1.0, END)
        second_text.insert(END, encrypted_text)
        second_text.configure(state=DISABLED)
    else:  # decrypt
        if len(msg.strip()) % 4 != 0:
            show_error("Invalid input. Please enter a valid encrypted text.")
            return
        try:
            decoded_msg = msg.strip().encode("utf-8")
            decrypted_text = base64.b64decode(decoded_msg).decode("utf-8")
        except Exception:
            show_error("Invalid input. Please enter a valid encrypted text.")
            return
        second_text.configure(state=NORMAL)
        second_text.delete(1.0, END)
        second_text.insert(END, decrypted_text)
        second_text.configure(state=DISABLED)


def switch_action():
    global mode, first_text, second_text, action_btn

    # Grab whatever's currently in the output box
    output_content = second_text.get(1.0, END).strip()

    # Flip mode
    mode = "decrypt" if mode == "encrypt" else "encrypt"
    action_btn.configure(text=mode.capitalize(), bg=btn_color1 if mode == "encrypt" else btn_color2)


    # Move output -> input, then auto-run the new action
    first_text.delete(1.0, END)
    first_text.insert(END, output_content)

    if output_content:
        perform_action()

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

def show_error(message):
    second_text.configure(state=NORMAL)
    second_text.delete(1.0, END)
    second_text.insert(END, message, "error")
    second_text.configure(state=DISABLED)


# Main GUI Screen for Cipher Machine Tool
def machine_screen():
    global machine_screen, passcode, first_text, second_text, action_btn, fixed_font, btn_fixed_font

    save_password()

    machine_screen = Tk()
    machine_screen.geometry("400x420")
    machine_screen.title("Cipher Machine")
    machine_screen.minsize(420, 380)  # minimum window size
    machine_screen.configure(bg=main_bg)

    base_family = tkfont.nametofont("TkFixedFont").actual("family")
    fixed_font = tkfont.Font(family=base_family, size=13)
    btn_fixed_font = tkfont.Font(family=base_family, size=9)

    #Tkinter style rules for the whole application
    machine_screen.option_add("*Text.background", textbox_bg)
    machine_screen.option_add("*Text.foreground", main_text)
    machine_screen.option_add("*Text.insertBackground", main_text)
    machine_screen.option_add("*Text.relief", "flat")
    machine_screen.option_add("*Text.highlightThickness", 1)
    machine_screen.option_add("*Text.highlightBackground", textbox_bg)
    machine_screen.option_add("*Text.highlightColor", textbox_bg)

    machine_screen.option_add("*Entry.background", textbox_bg)
    machine_screen.option_add("*Entry.foreground", main_text)
    machine_screen.option_add("*Entry.insertBackground", main_text)
    machine_screen.option_add("*Entry.relief", "flat")
    machine_screen.option_add("*Entry.highlightThickness", 1)
    machine_screen.option_add("*Entry.highlightBackground", textbox_bg)
    machine_screen.option_add("*Entry.highlightColor", textbox_bg)

    machine_screen.option_add("*Label.background", main_bg)
    machine_screen.option_add("*Label.foreground", main_text)
    machine_screen.option_add("*Font", fixed_font)


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
    machine_screen.rowconfigure(1, weight=1)
    machine_screen.rowconfigure(3, weight=1)

    def reset_machine():
        passcode.set("")
        first_text.delete(1.0, END)

    # Row 0: label
    Label(text="Enter Text:").grid(
        row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 0)
    )

    # Row 1: input box
    input_frame = Frame(machine_screen)
    input_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    input_frame.columnconfigure(0, weight=1)
    input_frame.rowconfigure(0, weight=1)

    first_text = Text(input_frame, bd=0, height=4)
    first_text.grid(row=0, column=0, sticky="nsew")
    in_scrollbar = ttk.Scrollbar(input_frame, orient=VERTICAL, command=first_text.yview, style="Custom.Vertical.TScrollbar")
    in_scrollbar.grid(row=0, column=1, sticky="ns")
    first_text.configure(yscrollcommand=in_scrollbar.set)

    # Row 2: action + switch buttons
    action_btn = Button(text=mode.capitalize(), bg=btn_color1, fg=main_text, bd=0, font=btn_fixed_font, command=perform_action)
    action_btn.grid(row=2, column=0, sticky="ew", padx=(20, 5), pady=5, ipady=10)
    Button(text="Switch", bg=btn_color6, fg=main_text, bd=0, font=btn_fixed_font, command=switch_action).grid(
        row=2, column=1, sticky="ew", padx=(5, 20), pady=5, ipady=10
    )

    # Row 3: output box
    output_frame = Frame(machine_screen)
    output_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)

    second_text = Text(output_frame, bd=0, height=4, state=DISABLED)
    second_text.tag_configure("error", foreground="#E06C75")
    second_text.grid(row=0, column=0, sticky="nsew")
    out_scrollbar = ttk.Scrollbar(output_frame, orient=VERTICAL, command=second_text.yview, style="Custom.Vertical.TScrollbar")
    out_scrollbar.grid(row=0, column=1, sticky="ns")
    second_text.configure(yscrollcommand=out_scrollbar.set)

    # Row 4: passcode label
    Label(text="Enter Passcode:").grid(
        row=4, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 0)
    )

    # Row 5: passcode entry + button
    passcode_frame = Frame(machine_screen, bg=main_bg)
    passcode_frame.grid(row=5, column=0, columnspan=2, sticky="w", padx=20, pady=5)

    passcode = StringVar()
    Entry_widget = Entry(passcode_frame, textvariable=passcode, width=25, font=fixed_font, show="*", bd=0)
    Entry_widget.pack(side=LEFT)
    Button(passcode_frame, text="Change Password", bg=btn_color6, relief=FLAT, fg=main_text, font=btn_fixed_font, activebackground=btn_color6, command=change_password).pack(side=LEFT, padx=(5, 0))


    Button(text="Reset", bg=btn_color3, fg=main_text, bd=0, font=btn_fixed_font, command=reset_machine).grid(
        row=6, column=0, columnspan=2, sticky="ew", padx=20, pady=5, ipady=10
    )
    Button(text="Save", bg=btn_color4, fg=main_text, bd=0, font=btn_fixed_font, command=save_text).grid(
        row=7, column=0, columnspan=2, sticky="ew", padx=20, pady=5, ipady=10
    )
    Button(text="Import File", bg=btn_color5, fg=main_text, bd=0, font=btn_fixed_font, command=import_file).grid(
        row=8, column=0, columnspan=2, sticky="ew", padx=20, pady=(5, 15)
    )

    machine_screen.mainloop()

# Display screen function when run is clicked
machine_screen()