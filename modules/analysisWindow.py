import time

from PySide6.QtCore import (Qt, QTimer, QDateTime)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton)

from modules.findPeakWindow import findPeakWindow
from modules.rootMeanWindow import rootMeanWindow
from modules.arquivo import arquivo
from database.db import *

import numpy as np
from modules.canvas import Canvas
import matplotlib.pyplot as plt

#Janela de gráfico dos arquivos externos
class analysisWindow(QWidget):
    
    def encontrar_picos(self, buffer, tempo):
        self.peakWindow = findPeakWindow(buffer, tempo)
        
        self.peakWindow.show()

    def root_mean(self, buffer, tempo):

        self.root_mean_window = rootMeanWindow(buffer, tempo)

        self.root_mean_window.show()

    def excluir_registro(self, id):

        conn = get_conn()

        try:
            delete_wav_data(conn=conn, id=id)
            print("Registro excluído com sucesso!") ##Adicionar alerta para confirmar e etc
        except Exception as e:
            print(e)
        conn.close()
            
    def __init__(self, id):
        super().__init__()

        self.setWindowTitle("Registros Salvos")


        self.file = arquivo()
        
        conn = get_conn()

        registro = select_wav_data(conn, id)

        nome = registro[0]
        
        duracao = registro[1]

        caminho = registro[3]

        sampleRate = registro[4]


        #array numpy de 0 até a duração ao passo de 1 divido pelo SR
        tempo = np.arange(0,duracao,1/sampleRate) 

       

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

        buffer = np.sqrt(buffer_quadrado)




        self.setWindowTitle("Arquivo expandido")

        

        layout = QVBoxLayout()

        string_label = f'{nome} #ID: {id}'

        self.label = QLabel(string_label)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     
        

        canva = Canvas()
        canva.ax.set_title(self.file.nome_arquivo)
        canva.ax.set_xlabel('Tempo [s]')
        canva.ax.set_ylabel('Amplitude [Hz]')

        canva.ax.plot(self.file.tempo, self.file.audioBuffer/10000)

        layout.addWidget(canva)

        botaoRMS = QPushButton('Calcular RMS')
        botaoRMS.clicked.connect(lambda: self.root_mean(buffer,tempo))


        botaoPeaks = QPushButton('Achar Picos')
        botaoPeaks.clicked.connect(lambda: self.encontrar_picos(buffer,tempo))
        

        botaoDelete = QPushButton('Excluir Registro')
        botaoDelete.clicked.connect(lambda: self.excluir_registro(id))

        layout.addWidget(botaoRMS)
        layout.addWidget(botaoPeaks)
        layout.addWidget(botaoDelete)
        

        
      



        self.setLayout(layout)

        self.setFixedSize(self.size())


    

        


