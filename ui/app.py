# Import necessary modules and libraries.
# Create a basic Tkinter application window.
# Add input fields for email credentials and buttons for actions.
# Implement button click handlers to trigger email retrieval and display notifications.
# Implement functions to generate notifications using plyer or similar libraries.
# Show pop-up notifications for new emails and summaries.

# app.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# from conf_app import *

def notification(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

# test
notification("test", "test")