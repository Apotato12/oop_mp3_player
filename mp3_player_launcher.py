import tkinter as tk
from mp3_player_oop_style import MP3PlayerCore
from mp3_widgets import PlayerControls, PlaylistDisplay, StatusDisplay, FolderButton 

class MP3PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player OOP stlye")
        self.root.geometry("600x500")
        
        self.player = MP3PlayerCore()
        
        self.create_widgets()
        
        self.player.load_songs(self.player.music_directory)
        self.update_playlist()
    def create_widgets(self):
        """Create and arrange all widgets"""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.status = StatusDisplay(self.main_frame, self)
        self.status.pack(fill=tk.X, pady=5)

        self.playlist_display = PlaylistDisplay(self.main_frame, self)
        self.playlist_display.pack(fill=tk.BOTH, expand=True, pady=5)
  
        self.controls = PlayerControls(self.main_frame, self)
        self.controls.pack(fill=tk.X, pady=5)

        self.folder_btn = FolderButton(self.main_frame, self)
        self.folder_btn.pack(fill=tk.X, pady=5)
    def update_playlist(self):
        self.playlist_display.listbox.delete(0, tk.END)
        for song in self.player.playlist:
            self.playlist_display.listbox.insert(tk.END, song)
        
        if self.player.playlist:
            self.playlist_display.listbox.selection_set(self.player.current_index)
    # Methods that connect widgets to core functionality
    def play_pause(self):
        self.player.play_pause()
        
    def stop(self):
        self.player.stop()
        
    def next_song(self):
        self.player.next_song()
        self.update_playlist()
        
    def prev_song(self):
        self.player.prev_song()
        self.update_playlist()
        
    def set_volume(self, value):
        self.player.set_volume(value)
        
    def play_selected(self):
        selection = self.playlist_display.listbox.curselection()
        if selection:
            self.player.current_index = selection[0]
    
    def load_songs_dialog(self):
        if self.player.load_songs_dialog():
            self.update_playlist()

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3PlayerApp(root)
    root.mainloop()

