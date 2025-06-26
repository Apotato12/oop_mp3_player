from mp3_player_oop_style import pygame , tkinter as tk  , os
from tkinter import ttk, filedialog, messagebox
from pygame import mixer

class PlayerControls(tk.Frame):
    def __init__(self, master, player, **kwargs):
        super().__init__(master, **kwargs)
        self.player = player
        
        self.play_btn = tk.Button(self, text="▶", command=self.player.play_pause)
        self.play_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(self, text="⏹", command=self.player.stop)
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.prev_btn = tk.Button(self, text="⏮", command=self.player.prev_song)
        self.prev_btn.grid(row=0, column=2, padx=5)

        self.next_btn = tk.Button(self, text="⏭", command=self.player.next_song)
        self.next_btn.grid(row=0, column=3, padx=5)

        self.volume_scale = tk.Scale(self, from_=0, to=100, orient='horizontal',
                                   command=self.player.set_volume)
        self.volume_scale.set(70)
        self.volume_scale.grid(row=0, column=4, padx=5)

class PlaylistDisplay(tk.Frame):
    def __init__(self, master, player, **kwargs):
        super().__init__(master, **kwargs)
        self.player = player
        
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set,
        selectbackground='lightblue', selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-1>', lambda e: self.player.play_selected())
        
        self.scrollbar.config(command=self.listbox.yview)

