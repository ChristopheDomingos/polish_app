import os
import requests
from utils.resource_generator import ResourceGenerator
from gtts import gTTS

class ResourceManager:
    def __init__(self):
        os.makedirs("assets/audio", exist_ok=True)
        os.makedirs("assets/images/vocab", exist_ok=True)
        self.generator = ResourceGenerator()

    def ensure_resource(self, local_path, url=None, text_for_audio=None, is_audio=False, is_image=False):
        """
        If the resource doesn't exist, try to download from URL.
        If no URL and resource is audio with text_for_audio, generate using gTTS.
        If no URL and resource is image with text, generate a placeholder image.
        """
        if os.path.exists(local_path):
            return local_path

        if url:
            # Download from URL
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    f.write(r.content)
                return local_path
            except Exception as e:
                print(f"Failed to download from {url}, error: {e}")

        # If no URL:
        if is_audio and text_for_audio:
            # Generate audio from text using gTTS
            tts = gTTS(text=text_for_audio, lang='pl')
            tts.save(local_path)
            return local_path

        if is_image and text_for_audio:
            # text_for_audio here is used as the word for the image
            self.generator.generate_placeholder_image(text_for_audio, local_path)
            return local_path

        # If we reach here, no way to generate resource
        return None