import time


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton)

from modules.dialogo import salvoDialog

from modules.canvas import Canvas

#Janela de gráfico dos arquivos externos
class figureWindow(QWidget):


            
    def __init__(self, file):
        super().__init__()

        layout = QVBoxLayout()

        self.label = QLabel(file.nome_arquivo)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     
        
      

        canva = Canvas()
        canva.ax.set_title(file.nome_arquivo)
        canva.ax.set_xlabel('Tempo [s]')
        canva.ax.set_ylabel('Amplitude [Hz]')

        canva.ax.plot(file.tempo, file.audioBuffer/10000)


        layout.addWidget(canva)

        botaoSalvar = QPushButton('Salvar')
        botaoSalvar.clicked.connect(lambda:self.salvar_imagem(file))

    

        layout.addWidget(botaoSalvar)

        self.setLayout(layout)

        self.setFixedSize(self.size())


    def salvar_imagem(self, file):
        
        file.salvar_figura()


        salvoDialog()

        self.close()

