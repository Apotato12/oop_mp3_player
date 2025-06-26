import tkinter as tk
import pygame
import os
from tkinter import *

class mp3_player_launcher:
    def __init__(self):
        self.root = tk.TK()
        self.root.title("MP3 Player Launcher")
        self.root.geometry("300x200")
        self.create_widgets()
        self.root.mainloop()

class widget:
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(master, text = "mp3 player launcher")