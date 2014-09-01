from abc import ABCMeta, abstractmethod
from yapsy.IPlugin import IPlugin

class AbstractJasperPlugin(IPlugin):
    __metaclass__ = ABCMeta
    def __init__(self):
        super(AbstractJasperPlugin, self).__init__()
    
    def activate(self):
        if self.is_available():
            super(AbstractJasperPlugin, self).activate()

    def is_available(self):
        return True

class SpeechHandlerPlugin(AbstractJasperPlugin):
    CATEGORY = "speechhandler"
    def __init__(self):
        super(SpeechHandlerPlugin, self).__init__()

    @abstractmethod
    def handle(self, phrase):
        pass

    @abstractmethod
    def get_phrases():
        pass

class EventHandlerPlugin(AbstractJasperPlugin):
    CATEGORY = "eventhandler"
    def __init__(self):
        super(EventHandlerPlugin, self).__init__()

    @abstractmethod
    def handle(self, phrase):
        pass

class STTPlugin(AbstractJasperPlugin):
    CATEGORY = "stt"
    def __init__(self):
        super(STTPlugin, self).__init__()

    @abstractmethod
    def transcribe(self, audio_data, language="en_US"):
        """
        Transcribes audio_data and returns text.
        """
        pass
    
    @abstractmethod
    def get_languages():
        """
        Returns a list of available languages.
        """
        pass

class TTSPlugin(AbstractJasperPlugin):
    CATEGORY = "tts"
    def __init__(self):
        super(TTSPlugin, self).__init__()

    @abstractmethod
    def synthesize(self, phrase, language="en_US"):
        """
        Synthesizes phrase and returns wave data.
        """
        pass

    @abstractmethod
    def get_languages():
        """
        Returns a list of available languages.
        """
        pass