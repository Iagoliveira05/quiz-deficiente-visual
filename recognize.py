import speech_recognition as sr
from speak import app_falar

microfone = sr.Recognizer()

def ouvir_microfone():
    #Habilita o microfone do usuário
    
    #usando o microfone
    with sr.Microphone() as source:
        
        #Chama um algoritmo de reducao de ruidos no som
        microfone.adjust_for_ambient_noise(source)
        
        #Armazena o que foi dito numa variavel
        audio = microfone.listen(source)
        try:
            
            #Passa a variável para o algoritmo reconhecedor de padroes
            frase = microfone.recognize_google(audio,language='pt-BR')
            frase = frase.capitalize()
            app_falar(f'Escutei: {frase}.')
            #Retorna a frase pronunciada
            return frase

        #Se nao reconheceu o padrao de fala, exibe a mensagem
        except sr.UnknownValueError:
            app_falar(f'Não entendi, repita.')
            return ouvir_microfone()

if __name__ == "__main__":
    ouvir_microfone()
