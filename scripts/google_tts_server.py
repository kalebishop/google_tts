#!/usr/bin/env python3

import os
import rospy
from mutagen.mp3 import MP3

from google_tts.srv import Speech, SpeechResponse

import google.cloud.texttospeech_v1beta1 as tts

class GoogleTTS:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = rospy.get_param("google_tts/google_auth_path")

        self.language = 'en-US'
        self.voice = 'en-US-Standard-C'

        self.voice_params = tts.VoiceSelectionParams(
            language_code=self.language,
            name=self.voice,
            ssml_gender = tts.SsmlVoiceGender.FEMALE
        )

        self.audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)
        self.client = tts.TextToSpeechClient()

        rospy.init_node('google_tts', anonymous=True)
        rospy.Service('google_tts', Speech, self.handle_request)

    def handle_request(self, request):
        res = SpeechResponse()

        text = "<speak><prosody pitch=\"+2st\">{}</prosody></speak>".format(request.text)
        text_input = tts.SynthesisInput(ssml=text)
        response = self.client.synthesize_speech(input=text_input, voice=self.voice_params, audio_config=self.audio_config)
        res.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tts.mp3")

        with open(res.filename, "wb") as out:
            out.write(response.audio_content)
        
        res.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tts.mp3")

        mp3_obj = MP3(res.filename)
        print(mp3_obj.info.length)
        res.duration = mp3_obj.info.length
        return res
if __name__ == "__main__":
    node = GoogleTTS()
    rospy.spin()