import sys
import sounddevice as sd
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class signalWindow(QWidget):
    def __init__(self, input_device):
        super().__init__()


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
        self.x_data = range(self.num_frames)
        self.y_data = [0] * self.num_frames


        # Configurações da entrada de áudio ao vivo
        self.sample_rate = 44100  # Taxa de amostragem em Hz
        self.block_size = 1024  # Tamanho do bloco de áudio

        # Plota o gráfico inicial
        self.line, = plt.plot(self.x_data, self.y_data)

        # Variáveis de controle de atualização
        self.update_counter = 0
        self.update_limit = 10  # Limite de atualizações antes de redesenhar o canvas

        # Inicia a captura de áudio ao vivo
        self.stream = sd.InputStream(callback=self.callback, channels=1, samplerate=self.sample_rate, blocksize=self.block_size)
        self.stream.start()


        self.setLayout(layout)


        

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

        


        

        

        