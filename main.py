from tkinter import *
from tkinter import font

from speak import tocar_audio
from speak import app_falar
from recognize import ouvir_microfone

from time import sleep
import sys

class TelaInicial:
    def __init__(self):
        self.root = root
        self.configure()
        self.widgets()

        root.mainloop()
    
    def configure(self):
        self.root.attributes('-fullscreen', True)

        fundo = Label(self.root)
        fundo.la = PhotoImage(file='dependences/images/telaInicial.png')
        fundo['image'] = fundo.la
        fundo.place(x=0,y=0, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())

    def widgets(self):
        fonteBotao = font.Font(family="Berlin Sans FB Demi", size=30, weight=font.BOLD, underline=0, overstrike=0)

        lbJogar = Label(self.root, text="Jogar", font=fonteBotao, relief="flat", fg="#13112c", bg="#5454ce")
        lbJogar.place(relx=0.2, rely=0.718, width=309, height=92)

        lbTutorial = Label(self.root, text="Tutorial", font=fonteBotao, relief="flat", fg="#13112c", bg="#5454ce")
        lbTutorial.place(relx=0.595, rely=0.718, width=309, height=92)

        self.root.after(1000, lambda: self.audio("audioInicial.mp3"))

    def audio(self, nomeAudio):
        tocar_audio(nomeAudio)
        self.ouvirVoz()

    def ouvirVoz(self):
        resposta = ouvir_microfone()
        self.verificarResposta(resposta)

    def verificarResposta(self, resposta):
        if "jogar" in resposta.lower():
            self.mostrarTelaJogar()
        elif "tutorial" in resposta.lower():
            self.mostrarTelaTutorial()
        else:
            app_falar(f'Não entendi, repita!')
            self.ouvirVoz()

    def mostrarTelaJogar(self):
        self.entraTelaJogar()

    def mostrarTelaTutorial(self):
        self.entraTelaTutorial()

    def entraTelaJogar(self):
        self.subFrame = TelaJogo(self)
        self.hide()

    def entraTelaTutorial(self):
        self.subFrame = TelaTutorial(self)
        self.hide()

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.update()
        self.root.deiconify()


class TelaTutorial(Toplevel):
    def __init__(self, original):
        self.frame_original = original
        Toplevel.__init__(self)
        self.configure()
        self.widgets()

    def onClose(self):
        self.destroy()
        self.frame_original.show()

    def configure(self):
        self.attributes('-fullscreen', True)

        fundo = Label(self)
        fundo.la = PhotoImage(file='dependences/images/telaTutorial.png')
        fundo['image'] = fundo.la
        fundo.place(x=0,y=0, width=self.winfo_screenwidth(), height=self.winfo_screenheight())

    def widgets(self):
        fonteBotao = font.Font(family="Berlin Sans FB Demi", size=30, weight=font.BOLD, underline=0, overstrike=0)

        lbJogar = Label(self, text="Jogar", font=fonteBotao, relief="flat", fg="#13112c", bg="#5454ce")
        lbJogar.place(relx=0.566, rely=0.711, width=462, height=128)

        self.after(1000, lambda: self.audio("audioTutorial.mp3"))

    
    def audio(self, nomeAudio):
        tocar_audio(nomeAudio)
        tocar_audio("audioJogar.mp3")
        self.ouvirVoz()

    def ouvirVoz(self):
        resposta = ouvir_microfone()
        self.verificarResposta(resposta)

    def verificarResposta(self, resposta):
        if "jogar" in resposta.lower():
            self.mostrarTelaJogar()
        else:
            app_falar(f'Não entendi, repita')
            self.ouvirVoz()
    
    def mostrarTelaJogar(self):
        self.entraTelaJogar()

    def entraTelaJogar(self):
        self.subFrame = TelaJogo(self)
        self.hide()

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()


class TelaJogo(Toplevel):
    numeroDaPergunta = 1
    acertos = 0
    def __init__(self, original):
        self.frame_original = original
        Toplevel.__init__(self)
        self.configure()
        self.widgets()

    def onClose(self):
        self.destroy()
        self.frame_original.show()

    def configure(self):
        self.attributes('-fullscreen', True)

        fundo = Label(self)
        fundo.la = PhotoImage(file='dependences/images/telaPergunta.png')
        fundo['image'] = fundo.la
        fundo.place(x=0,y=0, width=self.winfo_screenwidth(), height=self.winfo_screenheight())

    def widgets(self):
        self.fonteTexto = font.Font(family="Arial MT", size=20, weight=font.BOLD, underline=0, overstrike=0)

        self.pergunta = StringVar()
        self.pergunta.set(self.selecionarPergunta(self.numeroDaPergunta))

        self.lbPergunta = Label(self, textvariable=self.pergunta, font=self.fonteTexto, fg="#13112c", bg="#fffcf3")
        self.lbPergunta.place(relx=0.065, rely=0.35, width=1340, height=150)

        self.after(1000, lambda: self.audio(f"perguntas/pergunta{self.numeroDaPergunta}.mp3"))

    def audio(self, nomeAudio):
        tocar_audio(nomeAudio)
        if self.numeroDaPergunta == 8:
            sleep(12)
        tocar_audio("audioAfirmacao.mp3")
        self.ouvirVoz()

    def ouvirVoz(self):
        resposta = ouvir_microfone()
        self.verificarResposta(resposta)

    def verificarResposta(self, resposta):
        if "sim" in resposta.lower():
            self.verificarAcerto("sim")
            self.proximaPergunta()
        elif "não" in resposta.lower():
            self.verificarAcerto("não")
            self.proximaPergunta()
        else:
            app_falar(f'Não entendi, repita')
            self.ouvirVoz()

    def verificarAcerto(self, respostaUsuario):
        resposta = respostaUsuario
        respostaCorreta = self.coletarRespostaCorreta(self.numeroDaPergunta)
        if resposta == respostaCorreta:
            self.acertos += 1

    def proximaPergunta(self):
        if self.numeroDaPergunta == 8:
            self.mostrarTelaFinal()            
        else:
            app_falar("Próxima pergunta!")
            self.numeroDaPergunta += 1
            self.pergunta.set(self.selecionarPergunta(self.numeroDaPergunta))
            self.update()
            self.audio(f"perguntas/pergunta{self.numeroDaPergunta}.mp3")

    def selecionarPergunta(self, numeroPergunta):
        with open(f"dependences/questions/pergunta{numeroPergunta}.txt", "r", encoding="utf-8") as arquivoPergunta:
            return arquivoPergunta.read()

    def coletarRespostaCorreta(self, numeroResposta):
        with open(f"dependences/answers/resposta{numeroResposta}.txt", "r", encoding="utf-8") as arquivoResposta:
            return arquivoResposta.read()
        
    def mostrarTelaFinal(self):
        self.entraTelaFinal()

    def entraTelaFinal(self):
        self.subFrame = TelaFinal(self, self.acertos)
        self.hide()

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()
        

class TelaFinal(Toplevel):
    def __init__(self, original, acertos):
        self.frame_original = original
        self.numeroDeAcertos = str(acertos)
        Toplevel.__init__(self)
        self.configure()
        self.widgets()

    def onClose(self):
        self.destroy()
        self.frame_original.show()

    def configure(self):
        self.attributes('-fullscreen', True)

        fundo = Label(self)
        fundo.la = PhotoImage(file='dependences/images/telaFinal.png')
        fundo['image'] = fundo.la
        fundo.place(x=0,y=0, width=self.winfo_screenwidth(), height=self.winfo_screenheight())

    def widgets(self):
        fonteBotao = font.Font(family="Berlin Sans FB Demi", size=30, weight=font.BOLD, underline=0, overstrike=0)
        fonteTexto = font.Font(family="Berlin Sans FB", size=55, weight=font.NORMAL, underline=0, overstrike=0)

        lbJogarNovamente = Label(self, text="Jogar Novamente", font=fonteBotao, fg="#13112c", bg="#5455ce")
        lbJogarNovamente.place(relx=0.192, rely=0.71, width=318, height=90)

        lbSair = Label(self, text="Sair", font=fonteBotao, fg="#13112c", bg="#5455ce")
        lbSair.place(relx=0.58, rely=0.71, width=318, height=90)

        lbAcertos = Label(self, text=f"ACERTOS: {self.numeroDeAcertos}/8", font=fonteTexto, fg="#13112c", bg="#fffdf3")
        lbAcertos.place(relx=0.053, rely=0.335, width=1370, height=115)

        self.after(1000, lambda: self.falarAcertos())

    def falarAcertos(self):
        app_falar(f"Você acertou: {self.numeroDeAcertos} de 8 perguntas!")
        self.audio("audioOpcoesFinais.mp3")

    def audio(self, nomeAudio):
        tocar_audio(nomeAudio)
        self.ouvirVoz()

    def ouvirVoz(self):
        resposta = ouvir_microfone()
        self.verificarResposta(resposta)

    def verificarResposta(self, resposta):
        if "jogar novamente" in resposta.lower():
            self.mostrarTelaJogo()
        elif "sair" in resposta.lower():
            sys.exit()
        else:
            app_falar(f'Não entendi, repita')
            self.ouvirVoz()

    def mostrarTelaJogo(self):
        self.entraTelaJogo()

    def entraTelaJogo(self):
        self.subFrame = TelaJogo(self)
        self.hide()

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()


if __name__ == "__main__":
    root = Tk()
    TelaInicial()
