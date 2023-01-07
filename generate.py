import time
import wave

import librosa
import librosa.display
from pydub import AudioSegment


def wav_read(path):
    y,sr = librosa.load(path)
    return y,sr
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
        for hz in range(0,20):
            if hz>16:
                element_text +="\033[31m"
            elif hz>8:
                element_text +='\033[33m'
            elif hz>0:
                element_text +='\033[32m'
            else:
                element_text +="\033[0m"
            for sound_element in sound_elements:
                if sound_element+30>3*hz:
                    element_text+="*"
                else:
                    element_text+= " "
            element_text+="\n"
        text.append(element_text)
    return text
def print_text(output_texts):
    for i in range(len(output_texts)):
        print(f"{output_texts[i]}\033[20A",end="")
        time.sleep(0.01)
    print('\n\n\n\n\n')
if __name__ == "__main__":
    path ="./loop_free.wav"
    if not is_channel_single(path):
        stereo2monoral(path)
        path="./formated.wav"

    y,sr = wav_read(path)
    stft_data = librosa.stft(y)
    magphase_data, phase = librosa.magphase(stft_data)
    db = librosa.amplitude_to_db(magphase_data)
    texts = sound2text(db.T)
    print_text(texts)