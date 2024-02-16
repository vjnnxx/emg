from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog)
from PySide6.QtGui import (QIcon, QFont)

import json

from modules.figureWindow import figureWindow
from modules.signalWindow import signalWindow


from database.db import (select_config_input_device, get_conn)

conn = get_conn()



#Janela de gráfico dos arquivos externos
class newAnalysis(QWidget):

     #Abre janela do windows para selecionar arquivos .wav
    def abrir_arquivo(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Audio (*.wav)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filename = dialog.selectedFiles()

            caminho = filename[0]
            

            self.abrir_janela_arquivo(caminho, self.id)


    def abrir_janela_arquivo(self, caminho, id):
        self.janela_arquivo = figureWindow(caminho, id)


        self.janela_arquivo.show()

    def abrir_janela_sinal(self):

        input_settings = select_config_input_device(conn)

        device = json.loads(input_settings[2])

        self.signal = signalWindow(device["id"])

        
        self.signal.show()


        
        

            
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Nova Análise')

        self.setWindowIcon(QIcon('./sound-wave.ico'))

        layout = QVBoxLayout()

        font = QFont()
        font.setPixelSize(60)

        self.label = QLabel('Escolha uma fonte')
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
      
        #Cria botão para abrir arquivo e adiciona botão ao layout
        botaoAbrir = QPushButton('Abrir arquivo')
        botaoAbrir.setFont(font)
        botaoAbrir.clicked.connect(self.abrir_arquivo)
        layout.addWidget(botaoAbrir)


        #Cria botão para gravar sinal e adiciona ao layout
        botaoGravar = QPushButton('Gravar Sinal')
        botaoGravar.setFont(font)
        botaoGravar.clicked.connect(self.abrir_janela_sinal)
        layout.addWidget(botaoGravar)
    

        self.setLayout(layout)

        self.setFixedSize(self.size())


    

        


