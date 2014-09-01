"""
Speech-To-Text implementation which relies on the Google Speech API.

This implementation requires a Google API key to be present in profile.yml

To obtain an API key:
1. Join the Chromium Dev group: https://groups.google.com/a/chromium.org/forum/?fromgroups#!forum/chromium-dev
2. Create a project through the Google Developers console: https://console.developers.google.com/project
3. Select your project. In the sidebar, navigate to "APIs & Auth." Activate the Speech API.
4. Under "APIs & Auth," navigate to "Credentials." Create a new key for public API access.
5. Add your credentials to your profile.yml. Add an entry to the 'keys' section using the key name 'GOOGLE_SPEECH.' Sample configuration:
6. Set the value of the 'stt_engine' key in your profile.yml to 'google'


Excerpt from sample profile.yml:

    ...
    timezone: US/Pacific
    stt_engine: google
    keys:
        GOOGLE_SPEECH: $YOUR_KEY_HERE

"""
import urllib2
import json
import traceback
from plugintypes import STTPlugin

class GoogleSTT(STTPlugin):

    RATE = 16000

    def __init__(self):
        super(GoogleSTT, self).__init__()
        # TODO: Get the API Key from config
        self.api_key = "ABC"

    def transcribe(self, audio_file_path, PERSONA_ONLY=False, MUSIC=False):
        """
            Performs STT via the Google Speech API, transcribing an audio file 
            and returning an English string.

            Arguments:
                audio_file_path -- the path to the .wav file to be transcribed
        """
        url = "https://www.google.com/speech-api/v2/recognize?output=json&client=chromium&key=%s&lang=%s&maxresults=6&pfilter=2" % (self.api_key, "en-us")

        wav = open(audio_file_path, 'rb')
        data = wav.read()
        wav.close()

        try:
            req = urllib2.Request(
                url,
                data=data,
                headers={
                    'Content-type': 'audio/l16; rate=%s' % GoogleSTT.RATE})
            response_url = urllib2.urlopen(req)
            response_read = response_url.read()
            response_read = response_read.decode('utf-8')
            decoded = json.loads(response_read.split("\n")[1])
            print response_read
            text = decoded['result'][0]['alternative'][0]['transcript']
            if text:
                print "==================="
                print "JASPER: " + text
                print "==================="
            return text
        except Exception:
            traceback.print_exc()

    def get_languages():
        # TODO: return a list of languages
        return ["en_US"]