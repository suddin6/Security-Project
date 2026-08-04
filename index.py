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
# Threading allows python to do more than one thing at a time, rather than waiting for one task to finish before starting another
# This allows us to have the little loading thing in the second text box
# The main "thread" is basically GUI and the background "thread" is the encryption math
# While it encrypts, main can animate the "Loading..."

from config import *
from crypto_logic import ALGORITHMS, DEFAULT_ALGORITHM, INPUT_TYPE, rsa_generate_keypair

from cryptography.hazmat.primitives import serialization

algorithm_var = None  # will become a StringVar once machine_screen() creates the window

# Encrypted and decrypted text outputs 
encrypted_text = ""
decrypted_text = ""

first_text = None
second_text = None

encrypt_btn = None
decrypt_btn = None

passcode_label = None
passcode_frame = None

shift_label = None
shift_frame = None
shift_var = None

rsa_public_key = ""
rsa_private_key = ""
rsa_key_screen = None

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

    algo_name = algorithm_var.get()
    input_type = INPUT_TYPE.get(algo_name, "passcode")
    key_input = ""

    if input_type == "passcode":
        key_input = passcode.get()
        if key_input == "":
            show_error("Please input a password to continue.")
            return
        if key_input != create_pw:
            show_error("Incorrect password.")
            return
    elif input_type == "number": # Caesar shift
        key_input = shift_var.get().strip()
        if key_input == "":
            show_error("Please enter a number to shift by.")
            return
    elif input_type == "keypair": # RSA
        key_input = rsa_public_key if mode == "encrypt" else rsa_private_key
        if key_input == "":
            show_error("Please set your RSA keys (Algorithm > Manage RSA Keys).")
            return

    msg = first_text.get(1.0, END)

    if len(msg.strip()) == 0:
        show_error(f"Please enter a text to {mode}.")
        return

    MAX_CHARS = 50000

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

        encrypt_func, decrypt_func = ALGORITHMS[algo_name]

        try:
            if mode == "encrypt":
                result = encrypt_func(msg, key_input)
                encrypted_text = result
            else:
                result = decrypt_func(msg, key_input)
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

        except Exception as error:
            error_message = str(error) if str(error) else "Invalid input. Please try again."

            def show_fail():
                stop_loading()
                show_error(error_message)
                encrypt_btn.configure(state=NORMAL)
                decrypt_btn.configure(state=NORMAL)

            machine_screen.after(0, show_fail)

    threading.Thread(target=do_work, daemon=True).start()

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







# Popup to manage RSA keys

def manage_rsa_keys():
    global rsa_public_key, rsa_private_key, rsa_key_screen

    if rsa_key_screen is not None and rsa_key_screen.winfo_exists():
        rsa_key_screen.lift()
        rsa_key_screen.focus_force()
        return

    rsa_key_screen = Toplevel(machine_screen)
    rsa_key_screen.title("Manage RSA Keys")
    rsa_key_screen.geometry("420x460")
    rsa_key_screen.minsize(380, 400)
    rsa_key_screen.configure(bg=main_bg)

    favicon = PhotoImage(file="favicon.png")
    rsa_key_screen.iconphoto(False, favicon)

    rsa_key_screen.columnconfigure(0, weight=1)
    rsa_key_screen.rowconfigure(1, weight=1)
    rsa_key_screen.rowconfigure(3, weight=1)

    Label(rsa_key_screen, text="Public Key (used to encrypt):", bg=main_bg, fg=main_text).grid(
        row=0, column=0, sticky="w", padx=15, pady=(15, 0)
    )
    public_frame = Frame(rsa_key_screen)
    public_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
    public_frame.columnconfigure(0, weight=1)
    public_frame.rowconfigure(0, weight=1)
    public_box = Text(public_frame, bd=0, wrap=WORD, height=6)
    public_box.grid(row=0, column=0, sticky="nsew")
    public_box.insert(END, rsa_public_key)
    pub_scrollbar = ttk.Scrollbar(public_frame, orient=VERTICAL, command=public_box.yview, style="Custom.Vertical.TScrollbar")
    pub_scrollbar.grid(row=0, column=1, sticky="ns")
    public_box.configure(yscrollcommand=pub_scrollbar.set)

    Label(rsa_key_screen, text="Private Key (used to decrypt):", bg=main_bg, fg=main_text).grid(
        row=2, column=0, sticky="w", padx=15, pady=(10, 0)
    )
    private_frame = Frame(rsa_key_screen)
    private_frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=5)
    private_frame.columnconfigure(0, weight=1)
    private_frame.rowconfigure(0, weight=1)
    private_box = Text(private_frame, bd=0, wrap=WORD, height=6)
    private_box.grid(row=0, column=0, sticky="nsew")
    private_box.insert(END, rsa_private_key)
    priv_scrollbar = ttk.Scrollbar(private_frame, orient=VERTICAL, command=private_box.yview, style="Custom.Vertical.TScrollbar")
    priv_scrollbar.grid(row=0, column=1, sticky="ns")
    private_box.configure(yscrollcommand=priv_scrollbar.set)

    def generate_new_keypair():
        public_pem, private_pem = rsa_generate_keypair()
        public_box.delete(1.0, END)
        public_box.insert(END, public_pem)
        private_box.delete(1.0, END)
        private_box.insert(END, private_pem)

    Button(rsa_key_screen, text="Generate New Keypair", bg=btn_color6, fg=main_text, bd=0, font=btn_fixed_font, command=generate_new_keypair).grid(
        row=4, column=0, sticky="ew", padx=15, pady=(5, 10), ipady=6
    )

    def save_keys():
        global rsa_public_key, rsa_private_key, rsa_key_screen

        new_public = public_box.get(1.0, END).strip()
        new_private = private_box.get(1.0, END).strip()

        if new_public:
            try:
                serialization.load_pem_public_key(new_public.encode("utf-8"))
            except Exception:
                messagebox.showerror("ERROR", "Invalid public key format.", parent=rsa_key_screen)
                return

        if new_private:
            try:
                serialization.load_pem_private_key(new_private.encode("utf-8"), password=None)
            except Exception:
                messagebox.showerror("ERROR", "Invalid private key format.", parent=rsa_key_screen)
                return

        rsa_public_key = new_public
        rsa_private_key = new_private
        rsa_key_screen.destroy()
        rsa_key_screen = None
        messagebox.showinfo("SUCCESS", "RSA keys have been set.", parent=machine_screen)

    def cancel_keys():
        global rsa_key_screen
        rsa_key_screen.destroy()
        rsa_key_screen = None

    btn_frame = Frame(rsa_key_screen, bg=main_bg)
    btn_frame.grid(row=5, column=0, sticky="ew", padx=15, pady=(0, 15))
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)
    Button(btn_frame, text="Save", bg=btn_color4, fg=main_text, bd=0, font=btn_fixed_font, command=save_keys).grid(
        row=0, column=0, sticky="ew", padx=(0, 5), ipady=8
    )
    Button(btn_frame, text="Cancel", bg=btn_color3, fg=main_text, bd=0, font=btn_fixed_font, command=cancel_keys).grid(
        row=0, column=1, sticky="ew", padx=(5, 0), ipady=8
    )


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
    pw_screen.geometry("320x320")
    pw_screen.minsize(300, 300)
    pw_screen.configure(bg=main_bg)

    favicon = PhotoImage(file="favicon.png")
    pw_screen.iconphoto(False, favicon)

    pw_screen.columnconfigure(0, weight=1)
    pw_screen.rowconfigure(4, weight=1)  # the checkbox row grows to fill extra space   

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

# Copy to Clipboard Functionality
def copy_input_text():
    text = first_text.get(1.0, END).strip()
    if not text:
        messagebox.showerror("ERROR", "There's nothing to copy yet.")
        return
    machine_screen.clipboard_clear()
    machine_screen.clipboard_append(text)
    machine_screen.update()
    messagebox.showinfo("SUCCESS", "Text copied to clipboard!")

def copy_output_text():
    text = second_text.get(1.0, END).strip()
    if not text or not has_valid_result:
        messagebox.showerror("ERROR", "There's nothing valid to copy yet.")
        return
    machine_screen.clipboard_clear()
    machine_screen.clipboard_append(text)
    machine_screen.update()
    messagebox.showinfo("SUCCESS", "Text copied to clipboard!")



def show_error(message):
    second_text.configure(state=NORMAL)
    second_text.delete(1.0, END)
    second_text.insert(END, message, "error")
    second_text.configure(state=DISABLED)







# Main GUI Screen for Cipher Machine Tool
def machine_screen():
    global machine_screen, passcode, first_text, second_text, fixed_font, btn_fixed_font, encrypt_btn, decrypt_btn, algorithm_var, passcode_label, passcode_frame, shift_label, shift_frame, shift_var

    save_password()

    machine_screen = Tk()
    algorithm_var = StringVar(value=DEFAULT_ALGORITHM)
    machine_screen.geometry("400x420")
    machine_screen.title("Cipher Machine")
    machine_screen.minsize(500, 500)  # minimum window size
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
    algo_menu = Menu(menu_bar, tearoff=0)
    algo_menu.add_command(label="Change Password...", command=change_password)
    algo_menu.add_separator()
    for algo_name in ALGORITHMS:
        algo_menu.add_radiobutton(label=algo_name, variable=algorithm_var, value=algo_name)
    algo_menu.add_separator()
    algo_menu.add_command(label="Manage RSA Keys...", command=manage_rsa_keys)
    menu_bar.add_cascade(label="Algorithm", menu=algo_menu)


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
    machine_screen.rowconfigure(4, weight=1)

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

    #Row 2: Copy input text
    Button(text="Copy", bg=btn_color6, fg=main_text, bd=0, font=btn_fixed_font, command=copy_input_text).grid(
        row=2, column=0, columnspan=2, sticky="e", padx=20, pady=(0, 5), ipady=0
    )

    # Row 3: encrypt/decrypt buttons
    encrypt_btn = Button(text="Encrypt", bg=btn_color1, fg=main_text, bd=0, font=btn_fixed_font, command=lambda: perform_action("encrypt"))
    encrypt_btn.grid(row=3, column=0, sticky="ew", padx=(20, 5), pady=5, ipady=10)
    decrypt_btn = Button(text="Decrypt", bg=btn_color2, fg=main_text, bd=0, font=btn_fixed_font, command=lambda: perform_action("decrypt"))
    decrypt_btn.grid(row=3, column=1, sticky="ew", padx=(5, 20), pady=5, ipady=10)

    # Row 4: output box
    output_frame = Frame(machine_screen)
    output_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)

    second_text = Text(output_frame, bd=0, height=4, state=DISABLED, undo=False)
    second_text.tag_configure("error", foreground="#E06C75")
    second_text.grid(row=0, column=0, sticky="nsew")
    out_scrollbar = ttk.Scrollbar(output_frame, orient=VERTICAL, command=second_text.yview, style="Custom.Vertical.TScrollbar")
    out_scrollbar.grid(row=0, column=1, sticky="ns")
    second_text.configure(yscrollcommand=out_scrollbar.set)

    # Row 5: Copy output text
    Button(text="Copy", bg=btn_color6, fg=main_text, bd=0, font=btn_fixed_font, command=copy_output_text).grid(
        row=5, column=0, columnspan=2, sticky="e", padx=20, pady=(0, 5), ipady=0
    )

    # Row 6: passcode label
    passcode_label = Label(text="Enter Passcode:")
    passcode_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 0))

    # Row 7: passcode entry + button
    passcode_frame = Frame(machine_screen, bg=main_bg)
    passcode_frame.grid(row=7, column=0, columnspan=2, sticky="w", padx=20, pady=5)

    passcode = StringVar()
    Entry_widget = Entry(passcode_frame, textvariable=passcode, width=21, font=fixed_font, show="*", bd=0)
    Entry_widget.pack(side=LEFT)
    

    show_passcode = BooleanVar(value=False)

    def toggle_passcode_visibility():
        Entry_widget.configure(show="" if show_passcode.get() else "*")

    Checkbutton(
        passcode_frame, text="Show", variable=show_passcode,
        bg=main_bg, fg=main_text, selectcolor=textbox_bg,
        activebackground=main_bg, activeforeground=main_text,
        command=toggle_passcode_visibility
    ).pack(side=LEFT, padx=(5, 0))

    Button(passcode_frame, text="Change Password", bg=btn_color6, relief=FLAT, fg=main_text, font=btn_fixed_font, activebackground=btn_color6, command=change_password).pack(side=LEFT, padx=(5, 0))

    # Row 8: shift label
    shift_label = Label(text="Shift Amount:")
    shift_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 0))

    # Row 9: shift entry
    shift_frame = Frame(machine_screen, bg=main_bg)
    shift_frame.grid(row=9, column=0, columnspan=2, sticky="w", padx=20, pady=5)

    def validate_number_input(new_value):
        if new_value == "":
            return True  # allow clearing the field entirely
        return new_value.lstrip("-").isdigit()  # allow digits, and an optional leading minus sign

    validate_cmd = (machine_screen.register(validate_number_input), "%P")

    shift_var = StringVar()
    Entry(shift_frame, textvariable=shift_var, width=10, font=fixed_font, bd=0,
        validate="key", validatecommand=validate_cmd).pack(side=LEFT) 

    def update_key_input_visibility(*args):
        input_type = INPUT_TYPE.get(algorithm_var.get(), "passcode")

        if input_type == "passcode":
            passcode_label.grid()
            passcode_frame.grid()
        else:
            passcode_label.grid_remove()
            passcode_frame.grid_remove()

        if input_type == "number":
            shift_label.grid()
            shift_frame.grid()
        else:
            shift_label.grid_remove()
            shift_frame.grid_remove()

    algorithm_var.trace_add("write", update_key_input_visibility)
    update_key_input_visibility()

    #Row 10: Clear All Button
    Button(text="Clear All", bg=btn_color3, fg=main_text, bd=0, font=btn_fixed_font, command=reset_machine).grid(
        row=10, column=0, columnspan=2, sticky="ew", padx=20, pady=20, ipady=10
    )

    machine_screen.mainloop()

# Display screen function when run is clicked
machine_screen()