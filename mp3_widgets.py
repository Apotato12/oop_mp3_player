import tkinter as tk

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
        
        self.volume_label = tk.Label(self, text="Volume")
        self.volume_label.grid(row=0, column=5)
    
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

class StatusDisplay(tk.Frame):
    def __init__(self, master, player, **kwargs):
        super().__init__(master, **kwargs)
        self.player = player
        

    def update_time(self, value):
        pass

class FolderButton(tk.Frame):
    def __init__(self, master, player, **kwargs):
        super().__init__(master, **kwargs)
        self.player = player
        
        self.load_btn = tk.Button(self, text="Load Music Folder",
                                   command=self.player.load_songs_dialog)
        self.load_btn.pack(fill=tk.X, pady=5)

# Example of how to integrate all components
class MP3Player(tk.Tk):
    def __init__(self, player):
        super().__init__()
        
        # Removed the title
        self.controls = PlayerControls(self, player)
        self.controls.pack(pady=10)
        
        self.playlist_display = PlaylistDisplay(self, player)
        self.playlist_display.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_display = StatusDisplay(self, player)
        self.status_display.pack(fill=tk.X, pady=10)
        
        self.folder_button = FolderButton(self, player)
        self.folder_button.pack(fill=tk.X, pady=10)



if __name__ == "__main__":
    # player is your media handling object
    player = None  # Replace with your actual player instance
    app = MP3Player(player)
    app.player.play_song(app.player.playlist[0])
    app.mainloop()
