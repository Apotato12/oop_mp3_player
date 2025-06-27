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
        self.current_song = None
        return False

    def play_song(self, song):
        if song:
            print(f"Playing: {song}")
            full_path = os.path.join(self.music_directory, song)
            mixer.music.load(full_path)
            mixer.music.play()
            self.is_playing = True
            self.paused = False

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
            print(f"Paused: {self.current_song}")
        else:
            if self.paused:
                mixer.music.unpause()
                self.is_playing = True
                self.paused = False
                print(f"Resumed: {self.current_song}")
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
        print("Playback stopped")

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
        print(f'Setting volume to: {volume}')
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
        return mixer.Sound(os.path.join(self.music_directory, self.current_song)).get_length() if self.current_song else 0


class MP3PlayerGUI:
    def __init__(self, master):
        self.master = master
        self.player = MP3PlayerCore()

        # Now Playing Label
        self.now_playing_label = Label(master, text="Now Playing: No song selected")
        self.now_playing_label.pack(pady=10)
        
        # Progress Bar
        self.progress_var = DoubleVar()
        self.progress_bar = Scale(master, from_=0, to=100, variable=self.progress_var, orient=HORIZONTAL, command=self.set_position)
        self.progress_bar.pack(fill=X)
        
        # Play/Pause Button
        self.play_button = Button(master, text="Play/Pause", command=self.player.play_pause)
        self.play_button.pack()
        
        # Stop Button
        self.stop_button = Button(master, text="Stop", command=self.player.stop)
        self.stop_button.pack()
        
        # Next Button
        self.next_button = Button(master, text="Next", command=self.player.next_song)
        self.next_button.pack()
        
        # Previous Button
        self.prev_button = Button(master, text="Previous", command=self.player.prev_song)
        self.prev_button.pack()
        
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
        value = int(value)
        duration = self.player.get_duration()
        if duration > 0:
            new_position = (value / 100) * duration
            mixer.music.set_pos(new_position)

    def show_duration(self):
        duration = self.player.get_duration()
        current_position = self.player.get_position()
        print(f"Current Time: {current_position:.2f}s / Duration: {duration:.2f}s")

    def update_ui(self):
        if self.player.is_playing:
            current_position = self.player.get_position()
            duration = self.player.get_duration()
            self.progress_var.set((current_position / duration) * 100 if duration > 0 else 0)

            self.update_now_playing()
            self.show_duration()
        
        self.master.after(1000, self.update_ui)


if __name__ == "__main__":
    root = Tk()
    root.title("MP3 Player")
    app = MP3PlayerGUI(root)
    root.mainloop()
