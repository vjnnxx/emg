import time


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox)

from modules.dialogo import salvoDialog

from modules.canvas import Canvas

#Janela de gráfico dos arquivos externos
class figureWindow(QWidget):


            
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel('Escolha um dos dispositivos disponíveis')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     
        
      





        botaoAnalise = QPushButton('Análise')
        botaoAnalise.clicked.connect(self.analise)

      

        layout.addWidget(botaoAnalise)


        self.setLayout(layout)


   
