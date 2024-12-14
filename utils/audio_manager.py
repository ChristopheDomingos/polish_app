import os
import pygame
from utils.resource_manager import ResourceManager

class AudioManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.res_manager = ResourceManager()

    def play_audio(self, text, url=None):
        if not text:
            return
        audio_dir = "assets/audio"
        os.makedirs(audio_dir, exist_ok=True)
        audio_file = os.path.join(audio_dir, f"{hash(text)}.mp3")

        # Ensure audio resource
        self.res_manager.ensure_resource(
            audio_file, url=url, text_for_audio=text, is_audio=True
        )

        if os.path.exists(audio_file):
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()