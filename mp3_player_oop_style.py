import pygame
import os
from tkinter import *
from pygame import mixer


class MP3PlayerCore:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.playing = False
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
        """Toggle between play and pause"""
        if not self.current_song and self.playlist:
            self.current_song = self.playlist[self.current_index]
        
        if self.paused:
            mixer.music.unpause()
            self.paused = False
        elif self.playing:
            mixer.music.pause()
            self.paused = True
    def play(self):
        """Play the current song"""
        if self.current_song:
            mixer.music.load(self.current_song)
            mixer.music.play()
            self.playing = True
            self.paused = False
    def stop(self):
        """Stop playback"""
        mixer.music.stop()
        self.playing = False
        self.paused = False
    def next_song(self):
        """Play the next song in playlist"""
        if not self.playlist:
            return
    
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.current_song = self.playlist[self.current_index]
        self.stop()
        self.play()
    def prev_song(self):
        """Play the previous song in playlist"""
        if not self.playlist:
            return
            
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.current_song = self.playlist[self.current_index]
        self.stop()
        self.play()

    def set_volume(self, value):
        """Set volume level (0-100)"""
        volume = float(value) / 100
        mixer.music.set_volume(volume)
    def get_current_song_name(self):
        """Return the name of the current song."""
        return os.path.basename(self.current_song) if self.current_song else "No song selected"
    def load_songs_dialog(self):
        """Open folder dialog to load music"""
        from tkinter import filedialog
        directory = filedialog.askdirectory(initialdir=self.music_directory)
        if directory:
            return self.load_songs(directory)
        return False