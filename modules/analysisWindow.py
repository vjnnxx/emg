import time

from PySide6.QtCore import (Qt, QTimer, QDateTime)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton)

from modules.findPeakWindow import findPeakWindow
from modules.arquivo import arquivo
from database.db import *

from modules.canvas import Canvas
import matplotlib.pyplot as plt

#Janela de gráfico dos arquivos externos
class analysisWindow(QWidget):
    
    def encontrar_picos(self, buffer):
        self.peakWindow = findPeakWindow(buffer)
        
        self.peakWindow.show()
            
    def __init__(self, id):
        super().__init__()

        self.setWindowTitle("Registros Salvos")


        self.file = arquivo()
        
        conn = get_conn()

        registro = select_wav_data(conn, id)


        caminho = registro[3]

        self.file.tratar_wav(caminho)



        buffer = select_buffer_wav_data(conn, id)

        buffer = json.loads(buffer[0])

        buffer = np.array(buffer)

        tamanho = np.size(buffer)

        buffer = buffer/10000


        '''Cálculo do RMS'''

        buffer_quadrado = buffer ** 2

        soma_quadrados = np.sum(buffer_quadrado)

        media = soma_quadrados/tamanho

        raiz_quadrada_media = np.sqrt(media)

        buffer = np.sqrt(buffer)



        self.setWindowTitle("Arquivo expandido")

        

        layout = QVBoxLayout()

        self.label = QLabel("Trabalhando")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     
        

        canva = Canvas()
        canva.ax.set_title(self.file.nome_arquivo)
        canva.ax.set_xlabel('Tempo [s]')
        canva.ax.set_ylabel('Amplitude [Hz]')

        canva.ax.plot(self.file.tempo, self.file.audioBuffer/10000)

        layout.addWidget(canva)

        botaoRMS = QPushButton('Calcular RMS')


        botaoPeaks = QPushButton('Achar Picos')
        botaoPeaks.clicked.connect(lambda: self.encontrar_picos(buffer_quadrado))

        layout.addWidget(botaoRMS)
        layout.addWidget(botaoPeaks)
        

        
      



        self.setLayout(layout)

        self.setFixedSize(self.size())


    

        


