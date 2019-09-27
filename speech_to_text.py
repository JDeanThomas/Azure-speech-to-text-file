#!/usr/bin/env python

import time
import wave

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python
    """)
    import sys
    sys.exit(1)

"""
File based peech from recognition Microsoft Cognitive Services Speech API
"""

# Set up the subscription info for the Speech Service:
speech_key, service_region = "YourSubscriptionKey", "YourServiceRegion"

def speech_to_text_continuous():
    """
    performs continuous speech recognition with input from an audio file
    """
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=inf)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """
        callback that stops continuous recognition upon receiving an event `evt`
        """
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    # Parse JSON output and assemble for writing to file


if __name__ == '__main__':
    speech_to_text_continuous()
    """ 
    Detects if the file input is stdin (called from a Bash pipeline
    from ffmpeg) or is being called dirrecty on a file.
    """
    if sys.stdin.isatty():
        filename = sys.argv[-1]
        inf = open(filename, 'rb')
        out = speech_to_text_continuous(inf)
        inf.close()
        file_out = open(filename + '_text.txt', 'w')
        file_out.write(str(out))
        file_out.close()
    else:
        inf = sys.stdin.buffer.read()
        out = speech_to_text_continuous(inf)
        print(out)