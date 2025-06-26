import tkinter as tk
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