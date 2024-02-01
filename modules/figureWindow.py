from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton)
from PySide6.QtGui import (QIcon)

from modules.dialogo import customDialog
from modules.arquivo import arquivo

from modules.canvas import Canvas
import matplotlib.pyplot as plt

#Janela de gráfico dos arquivos externos
class figureWindow(QWidget):

            
    def __init__(self, caminho):
        super().__init__()
        self.setWindowIcon(QIcon('./sound-wave.ico'))
        
        self.file = arquivo()

        self.setWindowTitle("Gráfico de arquivo externo")

        self.file.tratar_wav(caminho)

        layout = QVBoxLayout()

        self.label = QLabel(self.file.nome_arquivo)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     
        
      

        canva = Canvas()
        canva.ax.set_title(self.file.nome_arquivo)
        canva.ax.set_xlabel('Tempo [s]')
        canva.ax.set_ylim(-4,4)
        canva.ax.set_ylabel('Amplitude [Hz]')

        canva.ax.plot(self.file.tempo, self.file.audioBuffer/10000)


        layout.addWidget(canva)

        botaoSalvar = QPushButton('Salvar')
        botaoSalvar.clicked.connect(self.salvar_imagem)

    

        layout.addWidget(botaoSalvar)

        self.setLayout(layout)

        self.setFixedSize(self.size())


    def salvar_imagem(self):
        
        self.file.salvar_figura()


        customDialog("Figura salva com sucesso!")

        plt.close('all')

        self.close()

        


