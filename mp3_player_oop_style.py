import pygame
import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer

class MP3PlayerCore:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.is_playing = False
        self.paused = False
        self.current_song = None
        self.playlist = []
        self.current_index = 0
        self.music_directory = os.path.expanduser('~/Music')

    def load_songs(self, directory):
        """Load all supported audio files from directory"""
        self.music_directory = directory
        self.playlist = []
        os.chdir(directory)
        
        for file in os.listdir(directory):
            if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                self.playlist.append(file)
        
        if self.playlist:
            self.current_index = 0
            self.current_song = self.playlist[self.current_index]
            return True
        return False

    def play_pause(self):
        if not self.current_song and self.playlist:
            self.current_song = self.playlist[self.current_index]
        if not self.current_song:
            self.play()
        
        if self.paused:
            mixer.music.unpause()
            self.paused = False
        elif self.is_playing:  # Update here too
            mixer.music.pause()
            self.paused = True
        else:
            self.play()

    def play(self):
        """Play the current song"""
        if self.current_song:
            full_path = os.path.join(self.music_directory, self.current_song)
            mixer.music.load(full_path)
            mixer.music.set_volume(0.5)
            mixer.music.play()
            self.playing = True
            self.paused = False

    def stop(self):
        """Stop playback"""
        mixer.music.stop()
        self.is_playing = False  # Update here too
        self.paused = False
        self.current_song = None

    def next_song(self):
        """Play the next song in the playlist"""
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.current_song = self.playlist[self.current_index]
        self.stop()
        self.play()

    def prev_song(self):
        """Play the previous song in the playlist"""
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.current_song = self.playlist[self.current_index]
        self.stop()
        self.play()

    def set_volume(self, value):
        volume = max(0, min(float(value) / 100, 1))
        print(f'Setting volume to: {volume}')  # Debugging line
        try:
            mixer.music.set_volume(volume)
        except Exception as e:
            print(f'Error setting volume: {e}')

    def get_current_song_name(self):
        """Return the name of the current song."""
        return os.path.basename(self.current_song) if self.current_song else "No song selected"
    
    def load_songs_dialog(self):
        """Open folder dialog to load music"""
        directory = filedialog.askdirectory(initialdir=self.music_directory)
        if directory:
            return self.load_songs(directory)
        return False

class MP3PlayerGUI:
    def __init__(self, master):
        self.master = master
        self.player = MP3PlayerCore()
        
        # Now Playing Label
        self.now_playing_label = Label(master, text="Now Playing: ")
        self.now_playing_label.pack(pady=10)
        # Progress Bar
        self.progress_var = DoubleVar()
        self.progress_bar = Scale(master, from_=0, to=100, variable=self.progress_var, orient=HORIZONTAL, command=self.set_position)
        self.progress_bar.pack(fill=X)
        # Play/Pause Button
        self.play_button = Button(master, text="Play/Pause", command=self.player.play_pause)
        self.play_button.pack()
        # Load Music Folder Button
        self.load_button = Button(master, text="Load Music Folder", command=self.load_music_folder)
        self.load_button.pack()
        self.update_ui()
    def load_music_folder(self):
        if self.player.load_songs_dialog():
            self.update_now_playing()
    
    def update_now_playing(self):
        song_name = self.player.get_current_song_name()
        self.now_playing_label.config(text=f"Now Playing: {song_name}")
    def set_position(self, value):
        # Set the current position of the song
        value = int(value)
        self.player.mixer.music.set_pos(value)
    def update_ui(self):
        if self.player.playing:
            current_position = mixer.music.get_pos() / 1000  # Get current position in seconds
            self.progress_var.set(current_position)
        
            # Update song name in the label
            self.update_now_playing()
        
        # Schedule the update every second
        self.master.after(1000, self.update_ui)

if __name__ == "__main__":
    root = Tk()
    root.title("MP3 Player")
    app = MP3PlayerGUI(root)
    root.mainloop()
