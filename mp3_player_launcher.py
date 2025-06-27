import tkinter as tk
from mp3_player_oop_style import MP3PlayerCore
from mp3_widgets import PlayerControls, PlaylistDisplay, StatusDisplay, FolderButton 

class MP3PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player OOP Style")
        self.root.geometry("600x500")
        self.player = MP3PlayerCore()
        self.create_widgets()
        self.player.load_songs(self.player.music_directory)
        
        if self.player.playlist:
            self.update_playlist()
            self.player.current_index = 0 
            self.update_now_playing()  # Ensure this is called only if there are songs
            self._is_playing = False
            
        print("Loaded songs:", self.player.playlist)
        
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

        self.now_playing_label = tk.Label(self.main_frame, text="Now Playing: ")
        self.now_playing_label.pack(fill=tk.X, pady=5)

        self.update_progress_bar()

    def update_playlist(self):
        """Update the song list in the playlist display"""
        self.playlist_display.listbox.delete(0, tk.END)
        for song in self.player.playlist:
            self.playlist_display.listbox.insert(tk.END, song)
        
        if self.player.playlist:
            self.playlist_display.listbox.selection_set(self.player.current_index)
            self.update_now_playing()
    
    def update_now_playing(self):
       if self.player.playlist:
           current_song = self.player.playlist[self.player.current_index]
           self.now_playing_label.config(text=f"Now Playing: {current_song}")
       else:
           self.now_playing_label.config(text="Now Playing: No song selected")

    def update_progress_bar(self):
        if self.player.is_playing and self.player.current_song:  # Ensure a song is selected
            position = self.player.get_position()
            duration = self.player.get_duration()
            
            # Prevent division by zero
            if duration > 0:
                self.controls.progress_bar.set(position / duration * 100)
                self.controls.time_label.config(text=f"{position // 60}:{position % 60:02d} / {duration // 60}:{duration % 60:02d}")
        self.root.after(1000, self.update_progress_bar) 


    # Methods that connect widgets to core functionality
    def play_pause(self):
        self.player.play_pause()
        self.update_now_playing()

    def stop(self):
        self.player.stop()
        self.update_now_playing()

    def next_song(self):
        self.player.next_song()
        self.update_playlist()

    def prev_song(self):
        self.player.prev_song()
        self.update_playlist()

    def set_volume(self, value):
        self.player.set_volume(value)
        
    def play_selected(self):
        if not self.player.playlist:
           return
        selection = self.playlist_display.listbox.curselection()
        if selection:
            self.player.current_index = selection[0]
            self.player.play_song(self.player.playlist[self.player.current_index])
            self.update_now_playing()

    def load_songs_dialog(self):
       """Open a dialog to load new songs into the playlist"""
       try:
           if self.player.load_songs_dialog():
               self.update_playlist()
       except Exception as e:
           self.status.show_error(f"Error loading songs: {str(e)}")  # Assuming a method for displaying errors
   

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3PlayerApp(root)
    root.mainloop()
