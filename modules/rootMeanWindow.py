from PySide6.QtCore import (Qt, QTimer, QDateTime)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,QLabel, QPushButton, QLineEdit)
from PySide6.QtGui import (QDoubleValidator)

from scipy.signal import find_peaks
from modules.arquivo import arquivo

from modules.canvas import Canvas
import matplotlib.pyplot as plt

#Janela de gráfico dos arquivos externos
class rootMeanWindow(QWidget):

    def atualizar_valor(self, text):
        
        try:
            self.threshold = float(text)
        except Exception as e:
            self.threshold = 5
            print(e)

    def atualizar_canva(self):
        
        

        self.number_input.setText(str(self.threshold))

        self.canva.ax.clear()
        
        picos, _ = find_peaks(self.buffer, self.threshold)

        self.canva.ax.plot(self.buffer)
        
        self.canva.ax.plot(picos, self.buffer[picos], "x")

        self.canva.draw()

            
    def __init__(self, buffer_quadrado, tempo):
        super().__init__()


        self.buffer = buffer_quadrado

        self.tempo = tempo

        self.setWindowTitle("RMS")

       
        layout_horizontal = QHBoxLayout()   

        layout_canva = QVBoxLayout()

        self.label = QLabel("RMS")

        layout_canva.addWidget(self.label)

        layout_canva = QVBoxLayout()


        canva = Canvas()

        canva.ax.plot(self.tempo, self.buffer)

        layout_canva.addWidget(canva)

        layout_horizontal.addLayout(layout_canva)

        self.setLayout(layout_horizontal)

       
        self.setFixedSize(self.size())


    
        


