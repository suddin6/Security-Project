# Cipher Machine

A GUI-based encryption/decryption tool built with Python and Tkinter, for CSI 3480 - Security and Privacy in Computing.

**Authors:** Sumaya Uddin and Emma Hochron
**Professor:** Solmaz Salehian

## Description

Cipher Machine lets you encrypt and decrypt text using AES encryption (via the `cryptography` library), protected by your own passcode.

## Requirements

- Python 3.10 or later
- The `cryptography` package

## Setup

1. Clone or download this repository.
2. Install the required package:
   ```
   pip install -r requirements.txt
   ```
3. Run the program:
   ```
   python index.py
   ```

## First Launch

On first launch, you'll create a passcode. The passcode is required to use the application, and it can be changed later in the app as long as you remember your old password.

## Features

- Encrypt and decrypt text using AES encryption
- Import text from a `.txt` file
- Save encryption/decryption results to a chosen file, with an optional preview before saving
- Clear all saved messages
- Change your passcode at any time

## File Overview

| File | Purpose |
|---|---|
| `index.py` | Main application: GUI, password handling, saving/loading |
| `crypto_logic.py` | Encryption and decryption functions |
| `config.py` | Color scheme and styles |
| `favicon.png` | Application icon |
| `requirements.txt` | Python package dependencies |

`passwords.txt` and `saved_msgs.txt` are created automatically the first time you run the app.
