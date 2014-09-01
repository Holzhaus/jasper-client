"""
Dummy Speech-To-Text Engine.
"""

from plugintypes import STTPlugin

class DummySTT(STTPlugin):
    def __init__(self):
        super(DummySTT, self).__init__()

    def transcribe(self, audio_file_path, PERSONA_ONLY=False, MUSIC=False):
        return ""

    def get_languages():
        # TODO: return a list of languages
        return "en_US"