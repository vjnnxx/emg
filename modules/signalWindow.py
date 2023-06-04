import sys
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class signalWindow(QWidget):
    def __init__(self, input_device):
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
        botaoParar = QPushButton("Parar")

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

        


        

        

        