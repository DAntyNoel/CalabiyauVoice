from convert2wav import *
from csv_controller import *
from tencent_speech_recog import *

def get_recog_result(audio_file) -> str:
    wav_file = convert2wav(audio_file)
    return translate_wav(wavfile=wav_file)