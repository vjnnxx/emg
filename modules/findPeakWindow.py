from PySide6.QtCore import (Qt, QTimer, QDateTime)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,QLabel, QPushButton, QLineEdit)
from PySide6.QtGui import (QDoubleValidator)

from scipy.signal import find_peaks
from modules.arquivo import arquivo

from modules.canvas import Canvas
import matplotlib.pyplot as plt

#Janela de gráfico dos arquivos externos
class findPeakWindow(QWidget):

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

            
    def __init__(self, buffer_quadrado):
        super().__init__()


        self.buffer = buffer_quadrado
        

        self.threshold = 1
       

        self.setWindowTitle("Encontrar picos")

       
        layout_horizontal = QHBoxLayout()   

        layout_canva = QVBoxLayout()

        self.label = QLabel("Encontrar picos")
        self.label.setAlignment(Qt.AlignCenter)
        layout_canva.addWidget(self.label)


        ''' Achar picos'''

        self.canva = Canvas()
        
        picos, _ = find_peaks(self.buffer, self.threshold)

        self.canva.ax.plot(self.buffer)
        
        self.canva.ax.plot(picos, self.buffer[picos], "x")


        layout_canva.addWidget(self.canva)

        layout_horizontal.addLayout(layout_canva)


        layout_inputs = QVBoxLayout()

        self.number_input = QLineEdit() 
        #self.number_input.setValidator(QDoubleValidator(0.00, 3 ,2))
        self.number_input.textChanged.connect(self.atualizar_valor)
        

        botao = QPushButton('Encontrar')
        botao.clicked.connect(self.atualizar_canva)

        


        form_layout = QFormLayout()

        form_layout.addRow("Valor", self.number_input)
        form_layout.addRow("", botao)

        #layout_inputs.addWidget(number_input)

        #layout_inputs.addWidget(botao)

        layout_horizontal.addLayout(form_layout)
           
        

        self.setLayout(layout_horizontal)

        self.setFixedSize(self.size())


    
        


