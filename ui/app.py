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

import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

if __name__ == "__main__":
    from sfx import should_play_sound, sound_mail, already_playing
    from conf_app import *
else:
    from .conf_app import *
    from .sfx import should_play_sound, sound_mail, already_playing

def close_message_box(messagebox):
    global should_play_sound
    should_play_sound = False
    print("Close message box.")
    messagebox.destroy()

def msgbox(title, message):
    messagebox = tk.Tk()
    messagebox.title(title)

    messagebox.geometry(f"{BOX_WIDTH}x{BOX_HEIGHT}")
    
    v = tk.Scrollbar(messagebox, orient='vertical')
    v.pack(side='right', fill='y')

    close_button = tk.Button(messagebox, text="Close", command=lambda: close_message_box(messagebox))
    close_button.pack(pady=30)
    
    # label = tk.Label(messagebox, text=message, font=("SF Pro Display", 14), wraplength=BOX_WIDTH-200, justify="left", )
    # label.pack(padx=50, pady=50)
    text = tk.Text(messagebox, font=("SF Pro Display", 14), wrap="word", yscrollcommand=v.set)
    text.insert(tk.INSERT, message)
    text.pack(padx=50, pady=50)
    v.config(command=text.yview)

    messagebox.wm_attributes("-topmost", 1)
    messagebox.wm_attributes("-toolwindow", 1)
    messagebox.wm_attributes("-disabled", 0)
    
    messagebox.protocol("WM_DELETE_WINDOW", lambda: close_message_box(messagebox))
    
    messagebox.mainloop()

def sound_loop():
    print("sound loop")
    global should_play_sound
    global already_playing
    while should_play_sound:
        try:
            if not already_playing:
                already_playing = True
                sound_mail()
                time.sleep(20)
                already_playing = False
            else:
                print("already playing")
                break
        except:
            break
    print("sound loop end")

def notification(title, message):
    
    global should_play_sound
    should_play_sound = True
    thread_sound = threading.Thread(target=sound_loop)
    thread_window = threading.Thread(target=msgbox, args=(title, message))
    thread_sound.start()
    thread_window.start()

    thread_window.join()
    should_play_sound = False
    

# test
if __name__ == "__main__":
    notification("test", "long text "*200)