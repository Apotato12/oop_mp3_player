import pygame
import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import threading

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
        self.seek_position = 0  # Stores last known position
        self.song_duration = 0  # Cache song duration

    def load_songs(self, directory):
        self.music_directory = directory
        self.playlist = []
        os.chdir(directory)
        for file in os.listdir(directory):
            if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                self.playlist.append(file)
        if self.playlist:
            self.current_index = 0
            self.current_song = self.playlist[self.current_index]
            self.song_duration = mixer.Sound(os.path.join(directory, self.current_song)).get_length()
            return True
        self.current_song = None
        return False

    def play_song(self, song):
        if song:
            full_path = os.path.join(self.music_directory, song)
            mixer.music.load(full_path)
            mixer.music.play()
            self.is_playing = True
            self.paused = False
            self.song_duration = mixer.Sound(full_path).get_length()

    def play_selected(self):
        if 0 <= self.current_index < len(self.playlist):
            self.play_song(self.playlist[self.current_index])

    def play_pause(self):
        if not self.current_song and self.playlist:
            self.current_song = self.playlist[self.current_index]
        if not self.current_song:
            return
        if self.is_playing:
            self.paused = True
            mixer.music.pause()
            self.is_playing = False
        else:
            if self.paused:
                mixer.music.unpause()
                self.is_playing = True
                self.paused = False
            else:
                self.play()  # Play from the start

    def play(self):
        if self.current_song:
            self.play_song(self.current_song)

    def stop(self):
        mixer.music.stop()
        self.is_playing = False
        self.paused = False
        self.current_song = None

    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.current_song = self.playlist[self.current_index]
        self.stop()
        self.play()

    def prev_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.current_song = self.playlist[self.current_index]
        self.stop()
        self.play()

    def set_volume(self, value):
        volume = max(0, min(float(value) / 100, 1))
        try:
            mixer.music.set_volume(volume)
        except Exception as e:
            print(f'Error setting volume: {e}')

    def get_current_song_name(self):
        return os.path.basename(self.current_song) if self.current_song else "No song selected"

    def load_songs_dialog(self):
        directory = filedialog.askdirectory(initialdir=self.music_directory)
        if directory:
            return self.load_songs(directory)
        return False

    def get_position(self):
        return mixer.music.get_pos() / 1000

    def get_duration(self):
        return self.song_duration if self.current_song else 0

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

    def set_position(self, position):
        """Set the playback position without affecting audio quality"""
        try:
            mixer.music.set_pos(position)
        except Exception as e:
            print(f"Error seeking: {e}")

class MP3PlayerGUI:
    def __init__(self, master):
        self.master = master
        self.player = MP3PlayerCore()
        
        # UI Setup
        self.current_time_label = Label(master, text="00:00.000")
        self.current_time_label.pack()
        self.total_time_label = Label(master, text="00:00.000")
        self.total_time_label.pack()
        
        self.now_playing_label = Label(master, text="Now Playing: No song selected")
        self.now_playing_label.pack(pady=10)
        
        self.progress_var = DoubleVar()
        self.progress_bar = Scale(master, from_=0, to=100, orient=HORIZONTAL, 
                                command=self.on_progress_change)
        self.progress_bar.pack(fill=X)
        
        control_frame = Frame(master)
        control_frame.pack(pady=10)
        
        self.play_button = Button(control_frame, text="Play/Pause", command=self.play_pause)
        self.play_button.pack(side=LEFT, padx=5)
        
        self.stop_button = Button(control_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=LEFT, padx=5)
        
        self.prev_button = Button(control_frame, text="Previous", command=self.prev_song)
        self.prev_button.pack(side=LEFT, padx=5)
        
        self.next_button = Button(control_frame, text="Next", command=self.next_song)
        self.next_button.pack(side=LEFT, padx=5)
        
        self.load_button = Button(master, text="Load Music Folder", command=self.load_music_folder)
        self.load_button.pack(pady=10)
        
        self.update_ui()

    def on_progress_change(self, value):
        """Handle progress bar manipulation"""
        pos = float(value) / 100 * self.player.song_duration
        self.player.set_position(pos)
        self.update_time_display(pos)

    def update_time_display(self, position):
        self.current_time_label.config(text=self.player.format_time(position))
        self.total_time_label.config(text=self.player.format_time(self.player.song_duration))

    def update_ui(self):
        """Update the UI less frequently to reduce interference"""
        if self.player.is_playing:
            pos = self.player.get_position()
            self.progress_bar.set(min((pos / self.player.song_duration) * 100, 100))
            self.update_time_display(pos)
            self.now_playing_label.config(text=f"Now Playing: {self.player.get_current_song_name()}")
        
        self.master.after(100, self.update_ui)  # Reduced UI update frequency

    def load_music_folder(self):
        if self.player.load_songs_dialog():
            self.now_playing_label.config(text=f"Now Playing: {self.player.get_current_song_name()}")
            self.progress_bar.set(0)
            self.update_time_display(0)

    def play_pause(self):
        self.player.play_pause()
        self.update_ui()

    def stop(self):
        self.player.stop()
        self.update_ui()

    def next_song(self):
        self.player.next_song()
        self.update_ui()

    def prev_song(self):
        self.player.prev_song()
        self.update_ui()

if __name__ == "__main__":
    root = Tk()
    root.title("MP3 Player")
    app = MP3PlayerGUI(root)
    root.mainloop()
