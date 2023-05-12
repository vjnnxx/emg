from qdarktheme import load_stylesheet
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import ( 
    QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QMainWindow, QFileDialog)

from modules.functions import arquivo

import numpy as np

import os
import scipy.io
import scipy.io.wavfile

import matplotlib.pyplot as plt
import matplotlib




def printar():
    print('Botão foi clicado!')



#Janela principal do app
class Window(QMainWindow):


    def abrir_arquivo(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Audio (*.wav)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filename = dialog.selectedFiles()

            filename = filename[0]

            print(filename)

            file = arquivo()

            name = filename.split('/')
            name = name[-1]

            file = arquivo()

            file.path = filename

            dataset_path = os.path.join(file.path) 
            file.wavedata = os.path.join(dataset_path)

            file.sampleRate, file.audioBuffer = scipy.io.wavfile.read(file.wavedata)

            duracao = len(file.audioBuffer)/file.sampleRate


            tempo = np.arange(0,duracao,1/file.sampleRate)
            
            fig = plt.figure(figsize=(5,5), dpi=100)

            a = fig.add_subplot(111)

            a.plot(tempo, file.audioBuffer/10000)

            plt.xlabel('Tempo [s]')
            plt.ylabel('Amplitude [Hz]')
            plt.title(name)


            self.wid = QWidget()
            self.wid.resize(250, 150)
            self.wid.setWindowTitle('Arquivo Externo')
            self.wid.show()

            plt.show()



    def __init__(self):
        super().__init__()

        base = QWidget()
        layout = QVBoxLayout()


        #Criando barra de menu
        
        action = QAction('Ação', self)
        action.triggered.connect(printar)
        menu = self.menuBar()
        file_menu = menu.addMenu('Menu')
        file_menu.addAction(action)


        #Criando fonte e aplicando configurações
        font = QFont()
        font.setPixelSize(90)


        #Criando label
        self.label = QLabel('Salve Crias!')
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        botaoGravar = QPushButton('Abrir arquivo')
        botaoGravar.setFont(font)
        botaoGravar.clicked.connect(self.abrir_arquivo)
        layout.addWidget(botaoGravar)

        base.setLayout(layout)
        self.setCentralWidget(base)



app = QApplication()
app.setStyleSheet(load_stylesheet())

janela = Window()
janela.show()

app.exec()