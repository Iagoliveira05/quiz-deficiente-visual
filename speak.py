import random
from playsound import playsound
from gtts import gTTS
import os

def app_falar(audio):

    r1 = random.randint(1,1000000000)
    r2 = random.randint(1,1000000000)

    randfile = str(r2)+"randomtext"+str(r1) +".mp3"

    tts = gTTS(audio,lang='pt-br')
    #Salva o arquivo de audio
    tts.save(randfile)
    #Da play ao audio
    playsound(randfile)
    os.remove(randfile)

def tocar_audio(audio):
    playsound(r"dependences/audios/"+audio)
