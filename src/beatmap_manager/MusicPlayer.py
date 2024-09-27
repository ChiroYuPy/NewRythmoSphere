import os
import pygame

class MusicPlayer:
    def __init__(self, app):
        self.app = app
        self.is_playing = False
        self.current_music = None
        self.fade_duration = 200
        self.gain_volume = 1.0
        self.music_volume = 0.2
        self.effects_volume = 1.0
        self.fading_factor = 0.0
        self.fade_start_time = None

        # Initialize Pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0)  # Start with volume at 0

    def load_music(self):
        # Load the music file from the beatmap
        path = self.app.beatmap_selected.song_path
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            self.current_music = path
        else:
            print("Music file not found.")

    def play(self):
        if self.current_music:
            pygame.mixer.music.play()
            self.is_playing = True
            self.fade_start_time = pygame.time.get_ticks()  # Record the start time for fading
            self.fading_factor = 0.0  # Reset fading factor when starting to play
        else:
            print("No music loaded. Please load a music file first.")

    def set_cursor(self, time):
        if self.current_music:
            pygame.mixer.music.set_pos(time)  # Requires a supported audio format
        else:
            print("No music loaded. Please load a music file first.")

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            pygame.mixer.music.set_volume(0)  # Reset volume when stopped
            self.fading_factor = 0.0  # Reset fading factor when stopped

    def restart(self):
        if self.current_music:
            self.stop()  # Stop any currently playing music
            self.play()  # Start playing again from the beginning
        else:
            print("No music loaded. Please load a music file first.")

    def set_conventional_volume(self, volume):
        """Set the conventional volume (0.0 to 1.0)."""
        self.gain_volume = max(0.0, min(1.0, volume))  # Clamp value between 0 and 1
        self.update_volume()  # Update the volume immediately with the current fading factor

    def update_volume(self):
        """Update the music volume based on conventional volume and fading factor."""
        effective_volume = self.gain_volume * self.music_volume * self.fading_factor
        pygame.mixer.music.set_volume(effective_volume)

    def update(self, dt):
        """Update the player, fading in the volume over time."""
        if self.is_playing and self.fade_start_time is not None:
            elapsed_time = pygame.time.get_ticks() - self.fade_start_time
            if elapsed_time < self.fade_duration:
                # Update the fading factor based on elapsed time
                self.fading_factor = elapsed_time / self.fade_duration
                self.update_volume()  # Update the volume with the new fading factor
            else:
                # Once fade is complete, set the fading factor to 1.0
                self.fading_factor = 1.0
                self.update_volume()  # Update the volume to the maximum effective volume
                self.fade_start_time = None  # Reset fade start time

# Usage example:
# app = ...  # Assume app is initialized with a selected beatmap
# player = MusicPlayer(app)
# player.load_music()
# player.set_conventional_volume(0.8)  # Set the conventional volume
# player.play()

# In your main loop, you would call:
# dt = ...  # Get the delta time (in milliseconds) from your game loop
# player.update(dt)
