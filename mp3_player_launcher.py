import tkinter as tk
from mp3_player_oop_style import MP3PlayerCore
from mp3_widgets import PlaylistDisplay, StatusDisplay, FolderButton

class BaseControl(tk.Button):
    def __init__(self, master, player, app, text, **kwargs):  # Add app parameter
        super().__init__(master, text=text, **kwargs)
        self.player = player  # Store player reference
        self.app = app  # Store app reference

    def perform_action(self):
        raise NotImplementedError("Subclasses should implement this!")

class PlayControl(BaseControl):
    def perform_action(self):
        self.player.play_pause()  # Now access player directly

class StopControl(BaseControl):
    def perform_action(self):
        self.player.stop()

class PrevControl(BaseControl):
    def perform_action(self):
        self.player.prev_song()
        self.app.update_now_playing()  # Call update_now_playing from app

class NextControl(BaseControl):
    def perform_action(self):
        self.player.next_song()
        self.app.update_now_playing()  # Call update_now_playing from app

class MP3PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player OOP Style")
        self.root.geometry("600x500")
        self.player = MP3PlayerCore()
        self.player.load_songs(self.player.music_directory)
        
        if self.player.playlist:
            self.update_playlist()
            self.player.current_index = 0 
            self.update_now_playing()
            
        print("Loaded songs:", self.player.playlist)
        
        self.on_progress_drag = False  # Flag to track ongoing drag

        self.create_widgets()  # Ensure widgets are created

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.status = StatusDisplay(self.main_frame, self)
        self.status.pack(fill=tk.X, pady=5)
        self.playlist_display = PlaylistDisplay(self.main_frame, self)
        self.playlist_display.pack(fill=tk.BOTH, expand=True, pady=5)

        # Use polymorphic controls
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(fill=tk.X, pady=5)

        # Create buttons with player reference and app reference
        self.play_btn = PlayControl(self.controls_frame, self.player, self, text="▶")
        self.stop_btn = StopControl(self.controls_frame, self.player, self, text="⏹")
        self.prev_btn = PrevControl(self.controls_frame, self.player, self, text="⏮")
        self.next_btn = NextControl(self.controls_frame, self.player, self, text="⏭")

        # Set commands
        self.play_btn.config(command=self.play_btn.perform_action)
        self.stop_btn.config(command=self.stop_btn.perform_action)
        self.prev_btn.config(command=self.prev_btn.perform_action)
        self.next_btn.config(command=self.next_btn.perform_action)

        # Pack the buttons
        self.play_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.folder_btn = FolderButton(self.main_frame, self)
        self.folder_btn.pack(fill=tk.X, pady=5)
        self.now_playing_label = tk.Label(self.main_frame, text="Now Playing: ")
        self.now_playing_label.pack(fill=tk.X, pady=5)
    
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(self.main_frame, from_=0, to=100, orient='horizontal',
                                      variable=self.progress_var, command=self.on_progress_change)
        self.progress_bar.pack(fill=tk.X, pady=5)
    
        # Bind events for drag start and end
        self.progress_bar.bind("<ButtonPress-1>", self.on_progress_press)
        self.progress_bar.bind("<ButtonRelease-1>", self.on_progress_release)
    
        self.duration_label = tk.Label(self.main_frame, text="00:00/00:00")
        self.duration_label.pack(fill=tk.X, pady=5)
        self.update_progress()

    def update_playlist(self):
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

    def update_progress(self):
        if self.player.is_playing and not self.on_progress_drag:  # Only update when not dragging
            current_position = self.player.get_position()
            duration = self.player.get_duration()
            
            if duration > 0:
                progress = min((current_position / duration) * 100, 100)
                self.progress_var.set(progress)  # Update the progress bar smoothly
            
            self.update_duration_label()
            
        self.root.after(100, self.update_progress)  # Update every 100ms

    def update_duration_label(self):
        current_position = self.player.get_position()
        duration = self.player.get_duration()
        if current_position and duration:
            self.duration_label.config(
                text=f"{self.player.format_time(current_position)}/{self.player.format_time(duration)}"
            )
        else:
            self.duration_label.config(text="00:00.00/00:00.00")

    def on_progress_press(self, event):
        """Called when user starts dragging the progress bar"""
        self.on_progress_drag = True

    def on_progress_change(self, value):
        """Called during progress bar dragging"""
        if self.on_progress_drag and self.player.song_duration > 0:
            seek_pos = float(value) / 100 * self.player.song_duration
            self.player.set_position(seek_pos)  # Seek to the new position
            self.update_time_display(seek_pos)

    def on_progress_release(self, event):
        """Called when user releases the progress bar"""
        self.on_progress_drag = False
        # Perform one final seek to ensure accuracy
        value = self.progress_var.get()
        if self.player.song_duration > 0:
            seek_pos = float(value) / 100 * self.player.song_duration
            self.player.set_position(seek_pos)

    def update_time_display(self, position):
        """Update time display without affecting playback"""
        if self.player.song_duration > 0:
            self.duration_label.config(
                text=f"{self.player.format_time(position)}/{self.player.format_time(self.player.song_duration)}"
            )

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
            self.update_progress()

    def load_songs_dialog(self):
       """Open a dialog to load new songs into the playlist"""
       try:
           if self.player.load_songs_dialog():
               self.update_playlist()
       except Exception as e:
           self.status.show_error(f"Error loading songs: {str(e)}")  

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3PlayerApp(root)
    root.mainloop()
