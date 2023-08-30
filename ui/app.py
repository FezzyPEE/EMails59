# Import necessary modules and libraries.
# Create a basic Tkinter application window.
# Add input fields for email credentials and buttons for actions.
# Implement button click handlers to trigger email retrieval and display notifications.
# Implement functions to generate notifications using plyer or similar libraries.
# Show pop-up notifications for new emails and summaries.

# app.py

import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from sfx import sound_mail, sound_guard, playsound
# from conf_app import *
if __name__ == "__main__":
    from sfx import sound_mail, sound_guard
else:
    from .sfx import sound_mail, sound_guard

playing_sound = False

def sound_loop():
    global playing_sound
    while playing_sound:
        try:
            sound_mail()
            time.sleep(10)
        except:
            break

def close_message_box(messagebox):
    global playing_sound
    playing_sound = False
    print("Close message box.")
    messagebox.destroy()

def msgbox(title, message):
    messagebox = tk.Tk()
    messagebox.title(title)
    
    label = tk.Label(messagebox, text=message)
    label.pack(padx=20, pady=20)
    
    close_button = tk.Button(messagebox, text="Close", command=lambda: close_message_box(messagebox))
    close_button.pack(pady=10)
    
    messagebox.protocol("WM_DELETE_WINDOW", lambda: close_message_box(messagebox))
    
    messagebox.mainloop()

def notification(title, message):
    
    thread_sound = threading.Thread(target=sound_loop)
    thread_window = threading.Thread(target=msgbox, args=(title, message))
    global playing_sound
    playing_sound = True
    thread_sound.start()
    thread_window.start()

    thread_window.join()
    

# test
notification("test", "test")