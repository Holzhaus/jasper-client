"""
The default Speech-To-Text implementation which relies on PocketSphinx.
"""
from plugintypes import STTPlugin
# quirky bug where first import doesn't work
try:
    import pocketsphinx as ps
except:
    import pocketsphinx as ps

class PocketSphinxSTT(STTPlugin):

    def __init__(self, lmd = "languagemodel.lm", dictd = "dictionary.dic",
                lmd_persona = "languagemodel_persona.lm", dictd_persona = "dictionary_persona.dic",
                lmd_music=None, dictd_music=None, **kwargs):
        """
            Initiates the pocketsphinx instance.

            Arguments:
            speaker -- handles platform-independent audio output
            lmd -- filename of the full language model
            dictd -- filename of the full dictionary (.dic)
            lmd_persona -- filename of the 'Persona' language model (containing, e.g., 'Jasper')
            dictd_persona -- filename of the 'Persona' dictionary (.dic)
        """

        super(PocketSphinxSTT, self).__init__()

        hmdir = "/usr/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k"

        if lmd_music and dictd_music:
            self.speechRec_music = ps.Decoder(hmm = hmdir, lm = lmd_music, dict = dictd_music)
        self.speechRec_persona = ps.Decoder(hmm=hmdir, lm=lmd_persona, dict=dictd_persona)
        self.speechRec = ps.Decoder(hmm=hmdir, lm=lmd, dict=dictd)

    def transcribe(self, audio_file_path, PERSONA_ONLY=False, MUSIC=False):
            """
                Performs STT, transcribing an audio file and returning the result.

                Arguments:
                audio_file_path -- the path to the audio file to-be transcribed
                PERSONA_ONLY -- if True, uses the 'Persona' language model and dictionary
                MUSIC -- if True, uses the 'Music' language model and dictionary
            """

            wavFile = open(audio_file_path, 'rb')
            wavFile.seek(44)

            if MUSIC:
                self.speechRec_music.decode_raw(wavFile)
                result = self.speechRec_music.get_hyp()
            elif PERSONA_ONLY:
                self.speechRec_persona.decode_raw(wavFile)
                result = self.speechRec_persona.get_hyp()
            else:
                self.speechRec.decode_raw(wavFile)
                result = self.speechRec.get_hyp()

            print "==================="
            print "JASPER: " + result[0]
            print "==================="

            return result[0]

    def get_languages(self):
        return ["en_US"]