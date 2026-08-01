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
import threading
# Threading allows python to do more thn one thing at a time, rather than waiting for one task to finish before starting another
# This allows us to have the little loading thing in the second text box
# The main "thread" is basically GUI and the background "thread" is the encryption math
# While it encrypts, main can animate the "Loading..."

from config import *
from crypto_logic import encrypt_text, decrypt_text

try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    raise ImportError(
        "The 'cryptography' package is required. Install it with: pip install cryptography"
    )

# Encrypted and decrypted text outputs 
encrypted_text = ""
decrypted_text = ""

first_text = None
second_text = None

encrypt_btn = None
decrypt_btn = None

# Variables to store passwords
create_pw = ""
change_pw = ""
old_pw = ""

# Encrypt and Decrypt screens
encrypt_screen = ""
decrypt_screen = ""


mode = "encrypt"  # global toggle state
save_file_path = "saved_msgs.txt"
has_valid_result = False

loading_job = None
loading_dots = 0

pw_screen = None

def choose_save_location():
    global save_file_path
    path = filedialog.asksaveasfilename(
        title="Choose Save Location",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        initialfile="saved_msgs.txt"
    )
    if path:
        save_file_path = path
        messagebox.showinfo("SUCCESS", f"Save location set to:\n{save_file_path}")


def animate_loading():
    global loading_job, loading_dots
    loading_dots = (loading_dots % 3) + 1
    second_text.configure(state=NORMAL)
    second_text.delete(1.0, END)
    second_text.insert(END, "Loading" + "." * loading_dots)
    second_text.configure(state=DISABLED)
    loading_job = machine_screen.after(400, animate_loading)

def stop_loading():
    global loading_job
    if loading_job is not None:
        machine_screen.after_cancel(loading_job)
        loading_job = None


def perform_action(selected_mode):
    global mode, has_valid_result, encrypted_text, decrypted_text

    mode = selected_mode
    has_valid_result = False
    secret_key = passcode.get()

    if secret_key == "":
        show_error("Please input a password to continue.")
        return
    if secret_key != create_pw:
        show_error("Incorrect password.")
        return

    msg = first_text.get(1.0, END)

    if len(msg.strip()) == 0:
        show_error(f"Please enter a text to {mode}.")
        return
    

    MAX_CHARS = 50000  # limit

    msg = first_text.get(1.0, END)

    if len(msg.strip()) > MAX_CHARS:
        show_error(f"Text is too long ({len(msg.strip())} characters). Please limit input to {MAX_CHARS} characters.")
        encrypt_btn.configure(state=NORMAL)
        decrypt_btn.configure(state=NORMAL)
        return

    

    encrypt_btn.configure(state=DISABLED)
    decrypt_btn.configure(state=DISABLED)
    animate_loading()

    def do_work():
        global encrypted_text, decrypted_text

        try:
            if mode == "encrypt":
                result = encrypt_text(msg)
                encrypted_text = result
            else:
                result = decrypt_text(msg)
                decrypted_text = result

            def show_result():
                global has_valid_result
                stop_loading()
                second_text.configure(state=NORMAL)
                second_text.configure(wrap=NONE)
                second_text.delete(1.0, END)
                second_text.insert(END, result)
                second_text.configure(wrap=WORD)
                second_text.configure(state=DISABLED)
                has_valid_result = True
                encrypt_btn.configure(state=NORMAL)
                decrypt_btn.configure(state=NORMAL)

            machine_screen.after(0, show_result)

        except Exception:
            def show_fail():
                stop_loading()
                show_error("Invalid input. Please enter a valid encrypted text.")
                encrypt_btn.configure(state=NORMAL)
                decrypt_btn.configure(state=NORMAL)
            machine_screen.after(0, show_fail)

    threading.Thread(target=do_work, daemon=True).start()
    # target=do_work means this second thread's job is to run do_work()
    # A "daemon thread" is a background process that can be killed immediately when the program closes
    # otherwise if someone closes the app while it's running there will be a delay



def clear_saved():
    global save_file_path
    if not os.path.exists(save_file_path):
        messagebox.showinfo("INFO", "There are no saved messages to clear.")
        return

    confirmed = messagebox.askyesno(
        "Confirm Clear",
        "Are you sure you want to clear your saved messages? This cannot be undone."
    )
    if confirmed:
        try:
            os.remove(save_file_path)
            messagebox.showinfo("SUCCESS", "Saved messages have been cleared.")
        except Exception as error:
            messagebox.showerror("ERROR", f"An error occurred: {str(error)}")

# Function to save messages to a text file
def save_text():
    global mode, save_file_path, has_valid_result

    if not has_valid_result:
        messagebox.showerror("ERROR", "There's nothing valid to save yet.")
        return

    original = first_text.get(1.0, END).strip()
    result = second_text.get(1.0, END).strip()

    if len(result) == 0:
        messagebox.showerror("ERROR", "There's nothing to save yet.")
        return

    confirm_screen = Toplevel(machine_screen)
    confirm_screen.title("Confirm Save")
    confirm_screen.geometry("320x320")
    confirm_screen.minsize(280, 280)
    confirm_screen.configure(bg=main_bg)

    favicon = PhotoImage(file="favicon.png")
    confirm_screen.iconphoto(False, favicon)

    confirm_screen.columnconfigure(0, weight=1)
    confirm_screen.rowconfigure(1, weight=1)

    Label(confirm_screen, text="Preview:", bg=main_bg, fg=main_text).grid(
        row=0, column=0, sticky="w", padx=15, pady=(15, 0)
    )

    preview_frame = Frame(confirm_screen)
    preview_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
    preview_frame.columnconfigure(0, weight=1)
    preview_frame.rowconfigure(0, weight=1)

    preview_box = Text(preview_frame, bd=0, wrap=WORD)
    preview_box.grid(row=0, column=0, sticky="nsew")
    preview_scrollbar = ttk.Scrollbar(preview_frame, orient=VERTICAL, command=preview_box.yview, style="Custom.Vertical.TScrollbar")
    preview_scrollbar.grid(row=0, column=1, sticky="ns")
    preview_box.configure(yscrollcommand=preview_scrollbar.set)

    include_original = BooleanVar(value=False)

    def update_preview():
        preview_box.delete(1.0, END)
        if include_original.get():
            preview_box.insert(END, f"Original: {original}\n{mode.capitalize()}ed: {result}\n")
        else:
            preview_box.insert(END, f"{mode.capitalize()}ed: {result}\n")

    update_preview()  # show default preview immediately

    Checkbutton(
        confirm_screen, text="Include original text", variable=include_original,
        bg=main_bg, fg=main_text, selectcolor=textbox_bg, activebackground=main_bg,
        activeforeground=main_text, command=update_preview
    ).grid(row=2, column=0, sticky="w", padx=15, pady=(5, 0))

    def confirm_save():
        try:
            file_exists = os.path.exists(save_file_path)
            with open(save_file_path, "a") as file:
                if not file_exists:
                    file.write("Here are your saved messages:\n")
                if include_original.get():
                    file.write(f"Original: {original}\n{mode.capitalize()}ed: {result}\n")
                else:
                    file.write(f"{mode.capitalize()}ed: {result}\n")
            confirm_screen.destroy()
            messagebox.showinfo("SUCCESS", "Text saved to file successfully!")
        except Exception as error:
            messagebox.showerror("ERROR", f"An error occurred: {str(error)}")

    btn_frame = Frame(confirm_screen, bg=main_bg)
    btn_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=15)
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    Button(btn_frame, text="Save", bg=btn_color4, fg=main_text, bd=0, font=btn_fixed_font, command=confirm_save).grid(
        row=0, column=0, sticky="ew", padx=(0, 5), ipady=8
    )
    Button(btn_frame, text="Cancel", bg=btn_color3, fg=main_text, bd=0, font=btn_fixed_font, command=confirm_screen.destroy).grid(
        row=0, column=1, sticky="ew", padx=(5, 0), ipady=8
    )

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
    global create_pw, pw_screen

    if not os.path.exists("passwords.txt"):
        return

    if pw_screen is not None and pw_screen.winfo_exists():
        pw_screen.lift()          # bring existing window to front
        pw_screen.focus_force()   # give it keyboard focus
        return

    pw_screen = Toplevel(machine_screen)
    pw_screen.title("Change Password")
    pw_screen.geometry("320x260")
    pw_screen.minsize(300, 240)
    pw_screen.configure(bg=main_bg)

    favicon = PhotoImage(file="favicon.png")
    pw_screen.iconphoto(False, favicon)

    pw_screen.columnconfigure(0, weight=1)

    Label(pw_screen, text="Old Password:", bg=main_bg, fg=main_text).grid(
        row=0, column=0, sticky="w", padx=15, pady=(15, 0)
    )
    old_pw_var = StringVar()
    Entry(pw_screen, textvariable=old_pw_var, show="*", bd=0).grid(
        row=1, column=0, sticky="ew", padx=15, pady=(0, 10)
    )

    Label(pw_screen, text="New Password:", bg=main_bg, fg=main_text).grid(
        row=2, column=0, sticky="w", padx=15, pady=(0, 0)
    )
    new_pw_var = StringVar()
    Entry(pw_screen, textvariable=new_pw_var, show="*", bd=0).grid(
        row=3, column=0, sticky="ew", padx=15, pady=(0, 10)
    )

    confirm_var = BooleanVar(value=False)
    Checkbutton(
        pw_screen, text="I'm sure I want to change my password (this cannot be undone)",
        variable=confirm_var, wraplength=280, justify=LEFT,
        bg=main_bg, fg=main_text, selectcolor=textbox_bg,
        activebackground=main_bg, activeforeground=main_text
    ).grid(row=4, column=0, sticky="w", padx=15, pady=(5, 10))

    def submit_change():
        global create_pw, pw_screen

        old_pw = old_pw_var.get()
        new_pw = new_pw_var.get()

        if not confirm_var.get():
            messagebox.showerror("ERROR", "Please confirm the checkbox to continue.", parent=pw_screen)
            return
        if old_pw != create_pw:
            messagebox.showerror("ERROR", "Your old password is incorrect.", parent=pw_screen)
            return
        if new_pw == "":
            messagebox.showerror("ERROR", "Please do not leave the new password blank.", parent=pw_screen)
            return

        try:
            with open("passwords.txt", "w") as file:
                file.write(new_pw)
            create_pw = new_pw
            pw_screen.destroy()
            pw_screen = None
            messagebox.showinfo("SUCCESS", "Password has been saved.", parent=machine_screen)
        except Exception as error:
            messagebox.showerror("ERROR", f"An error occurred: {str(error)}")

    btn_frame = Frame(pw_screen, bg=main_bg)
    btn_frame.grid(row=5, column=0, sticky="ew", padx=15, pady=(5, 15))
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    Button(btn_frame, text="Submit", bg=btn_color4, fg=main_text, bd=0, font=btn_fixed_font, command=submit_change).grid(
        row=0, column=0, sticky="ew", padx=(0, 5), ipady=8
    )

    def cancel_change():
        global pw_screen
        pw_screen.destroy()
        pw_screen = None

    Button(btn_frame, text="Cancel", bg=btn_color3, fg=main_text, bd=0, font=btn_fixed_font, command=cancel_change).grid(
        row=0, column=1, sticky="ew", padx=(5, 0), ipady=8
    )


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
    global machine_screen, passcode, first_text, second_text, fixed_font, btn_fixed_font, encrypt_btn, decrypt_btn

    save_password()

    machine_screen = Tk()
    machine_screen.geometry("400x420")
    machine_screen.title("Cipher Machine")
    machine_screen.minsize(460, 380)  # minimum window size
    machine_screen.configure(bg=main_bg)

    menu_bar = Menu(machine_screen)
    machine_screen.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Save...", command=save_text)
    file_menu.add_command(label="Clear Saved Messages...", command=clear_saved)
    file_menu.add_separator()
    file_menu.add_command(label="Choose Save Location...", command=choose_save_location)
    file_menu.add_separator()
    file_menu.add_command(label="Import Text...", command=import_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=machine_screen.destroy)
    menu_bar.add_cascade(label="File", menu=file_menu)

    base_family = tkfont.nametofont("TkFixedFont").actual("family")
    fixed_font = tkfont.Font(family=base_family, size=13)
    btn_fixed_font = tkfont.Font(family=base_family, size=11)

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

    first_text = Text(input_frame, bd=0, height=4, undo=False)
    first_text.grid(row=0, column=0, sticky="nsew")
    in_scrollbar = ttk.Scrollbar(input_frame, orient=VERTICAL, command=first_text.yview, style="Custom.Vertical.TScrollbar")
    in_scrollbar.grid(row=0, column=1, sticky="ns")
    first_text.configure(yscrollcommand=in_scrollbar.set)

    def on_input_change(event):
        global has_valid_result
        has_valid_result = False
        first_text.edit_modified(False)  # reset the flag so this event can fire again

    first_text.bind("<<Modified>>", on_input_change)

    # Row 2: encrypt/decrypt buttons
    encrypt_btn = Button(text="Encrypt", bg=btn_color1, fg=main_text, bd=0, font=btn_fixed_font, command=lambda: perform_action("encrypt"))
    encrypt_btn.grid(row=2, column=0, sticky="ew", padx=(20, 5), pady=5, ipady=10)
    decrypt_btn = Button(text="Decrypt", bg=btn_color2, fg=main_text, bd=0, font=btn_fixed_font, command=lambda: perform_action("decrypt"))
    decrypt_btn.grid(row=2, column=1, sticky="ew", padx=(5, 20), pady=5, ipady=10)

    # command=perform_action("encrypt") DOES NOT WORK!!! because Python runs the function immediately upon calling
    # 
    # 
    # lambda: perform_action("encrypt") is the same as saying
    #
    #def encrypt():
    #   perform_action("encrypt")
    #
    #encrypt()



    # Row 3: output box
    output_frame = Frame(machine_screen)
    output_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)

    second_text = Text(output_frame, bd=0, height=4, state=DISABLED, undo=False)
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


    Button(text="Clear All", bg=btn_color3, fg=main_text, bd=0, font=btn_fixed_font, command=reset_machine).grid(
        row=6, column=0, columnspan=2, sticky="ew", padx=20, pady=5, ipady=10
    )

    # Button(text="Save", bg=btn_color4, fg=main_text, bd=0, font=btn_fixed_font, command=save_text).grid(
    #     row=7, column=0, sticky="ew", padx=(20, 5), pady=5, ipady=10
    # )
    # Button(text="Clear Save", bg=btn_color2, fg=main_text, bd=0, font=btn_fixed_font, command=clear_saved).grid(
    #     row=7, column=1, sticky="ew", padx=(5, 20), pady=5, ipady=10
    # )

    # Button(text="Import Text", bg=btn_color5, fg=main_text, bd=0, font=btn_fixed_font, command=import_file).grid(
    #     row=8, column=0, columnspan=2, sticky="ew", padx=20, pady=(5, 15)
    # )

    machine_screen.mainloop()

# Display screen function when run is clicked
machine_screen()