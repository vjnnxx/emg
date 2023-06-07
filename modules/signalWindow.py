import sys
import os
import wave
import sounddevice as sd
import pyaudio
import numpy as np
import matplotlib.pyplot as plt

from modules.arquivo import arquivo
from modules.dialogo import salvoDialog

from PySide6.QtCore import (QThreadPool)
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class Player:

    def __init__(self):
        self.on = False

    
    def change_status(self, value):
        self.on = value

    def get_on(self):
        return self.on


class signalWindow(QWidget):
    
    #Roda a função iniciar_gravacao em uma thread diferente
    def rodar_gravador(self):
        self.thread_manager.start(self.iniciar_gravacao)


    def iniciar_gravacao(self):
        
        self.gravador.change_status(True)

        audio = pyaudio.PyAudio()

        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        frames = []

        print("Gravando áudio...")

        
        while self.gravador.get_on():
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        try:
            os.makedirs('./audio')
        except:
            pass

        #conta o número de arquivos na pasta audio para numerar os arquivos salvos
        lst = os.listdir('./audio') 
        number_files = len(lst)

        novo_arquivo = './audio/audio' + str(number_files) + '.wav' 

        sound_file = wave.open(novo_arquivo, 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()

        self.file.tratar_wav(novo_arquivo)

        self.file.salvar_figura()

        nome_str = 'audio' + str(number_files)

        #self.thread_manager.start(salvoDialog(nome_str + "Áudio gravado e salvo com sucesso!"))

        print('Gravação finalizada')

    
    def parar_gravacao(self):

        self.gravador.change_status(False)

        self.thread_manager.waitForDone()
    
    
    def __init__(self, input_device):

        self.file = arquivo()


        self.gravador = Player()

        #gerenciador de threads
        self.thread_manager = QThreadPool()

        super().__init__()


        self.setWindowTitle("Plot de Áudio ao Vivo")

        # Cria um layout vertical
        layout = QVBoxLayout()

        # Cria um FigureCanvas e adiciona ao layout
        
        
        self.figure = plt.figure()
        
        
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Variáveis do gráfico
        self.num_frames = 1000  # Número de frames a serem mostrados no gráfico
        self.zoom_factor = 2  # Fator de zoom in/out

        # Dados do gráfico
        self.x_data = np.arange(self.num_frames)
        self.y_data = np.zeros(self.num_frames)


        # Configurações da entrada de áudio ao vivo
        sample_rate = 44100  # Taxa de amostragem em Hz
        block_size = 1024  # Tamanho do bloco de áudio
        self.device = input_device

        # Define os limites do eixo y
        plt.ylim(-1, 1)  # Intervalo desejado para o eixo y

        # Define os limites do eixo x
        plt.xlim(0, self.num_frames)  # Intervalo desejado para o eixo x

        # Plota o gráfico inicial
        self.line, = plt.plot(self.x_data, self.y_data)
        self.line.set_color('green')

        # Variáveis de controle de atualização
        self.update_counter = 0
        self.update_limit = 10  # Limite de atualizações antes de redesenhar o canvas

        # Inicia a captura de áudio ao vivo
        self.stream = sd.InputStream(callback=self.callback, device=self.device,channels=1, samplerate=sample_rate, blocksize=block_size)
        self.stream.start()

        plt.xlabel("Tempo")
        plt.ylabel("Amplitude")

        botaoGravar = QPushButton("Gravar")
        botaoGravar.clicked.connect(self.rodar_gravador)
        botaoParar = QPushButton("Parar")
        botaoParar.clicked.connect(self.parar_gravacao)

        layout.addWidget(botaoGravar)
        layout.addWidget(botaoParar)


        self.setLayout(layout)

        self.setFixedSize(self.size())


        

    def update_plot(self, indata):
        # Atualiza os dados do gráfico
        self.y_data[:-1] = self.y_data[1:]  # Desloca os valores existentes para a esquerda
        self.y_data[-1] = indata  # Adiciona o novo valor no final

        # Atualiza o gráfico com os novos dados
        self.line.set_ydata(self.y_data)

        # Atualiza o canvas
        self.canvas.draw()


    # Função de callback para atualizar o gráfico do FigureCanvas
    def callback(self, indata, frames, time, status):
        self.update_plot(indata[0])  # Atualiza o gráfico com o primeiro valor do áudio

        


        

        

        