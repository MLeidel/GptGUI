# openvoc.py
import openai
import subprocess
import platform

def play_file(speech_file_path):
    ''' Play the audio file currently set
    different actions occur based on running OS '''
    playcmd = []
    if platform.system() == "Windows":
        playcmd = [speech_file_path,]
    else:
        playcmd = ['play', speech_file_path]
    subprocess.Popen(playcmd)

def textospeech(voc, fmt, fou, inp):
    ''' create the audio file
        get parameters from GUI
        and get response from openai
    voc = voice to use
    fmt = audio file format to use
    fou = file name to use
    inp = text to convert to speech
    VOICES:
    'alloy','ash','ballad','coral','echo','fable','nova','onyx','sage','shimmer'
    FORMATS:
    'mp3', 'mp3', 'opus', 'aac', 'flac', 'wav', 'pcm'
    EXAMPLE USE:
    openvoc.textospeech('nova', 'mp3', 'speech.mp3', 'Hello, this is nova speaking.')
    '''

    if not fou.endswith(fmt):
        return 1  # "Extension must agree with format"

    speech_file_path = fou

    try:
        with openai.audio.speech.with_streaming_response.create(
          model="gpt-4o-mini-tts",
          voice=voc,
          response_format=fmt,
          input=inp
        ) as response:
          response.stream_to_file(speech_file_path)
          play_file(speech_file_path)
          return 0  # success
    except Exception as e:
        return 2  # problems


