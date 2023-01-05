import time
import wave

import librosa
import librosa.display
import numpy as np
import scipy.io.wavfile
from pydub import AudioSegment


def wav_read(path):
    rate,data = scipy.io.wavfile.read(path)
    return rate,data
def is_channel_single(path:str):
    wf = wave.open(path, "r")
    return wf.getnchannels() ==1

def stereo2monoral(path:str):
    sound = AudioSegment.from_wav(path)
    sound = sound.set_channels(1)
    sound.export("./formated.wav", format="wav")
def sound2text(sound_list:list):
    text = []
    for sound_elements in sound_list:
        element_text = ""
        for hz in range(0,10):
            if hz>8:
                element_text +="\033[31m"
            elif hz>4:
                element_text +='\033[33m'
            elif hz>0:
                element_text +='\033[32m'
            else:
                element_text +="\033[0m"
            for sound_element in sound_elements:
                if sound_element+30>5*hz:
                    element_text+="*"
                else:
                    element_text+= " "
            element_text+="\n"
        text.append(element_text)
    return text
def print_text(output_texts):
    for i in range(len(output_texts)):
        print(f"{output_texts[i]}\033[10A",end="")
        time.sleep(0.01)
    print('\n')
if __name__ == "__main__":
    path ="./free.wav"
    if not is_channel_single(path):
        stereo2monoral(path)
        path="./formated.wav"

    rate,data = wav_read(path)
    data =data/32768
    fft_size = 1024
    hop_length = int(fft_size *2)
    amplitude = np.abs(librosa.core.stft(data,n_fft=fft_size,hop_length=hop_length))
    log_power = librosa.core.amplitude_to_db(amplitude)
    texts = sound2text(log_power)
    print_text(texts)