from qdarktheme import load_stylesheet
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import ( 
    QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QMainWindow, QFileDialog)

from modules.functions import arquivo

import numpy as np

import os



import matplotlib

import matplotlib.pyplot as plt

from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 




def printar():
    print('Botão foi clicado!')


class Canvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = fig.add_subplot(111)
        self.ax.set_xlabel('Tempo [s]')
        self.ax.set_ylabel('Amplitude [Hz]')
        
        super(Canvas, self).__init__(fig)

        

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

        canva.ax.plot(file.tempo, file.audioBuffer/10000)


        layout.addWidget(canva)

        botaoSalvar = QPushButton('Salvar')
        botaoSalvar.clicked.connect(lambda:self.salvar_imagem(file))

        layout.addWidget(botaoSalvar)


        self.setLayout(layout)


    def salvar_imagem(self, file):
        
        file.salvar_figura()





#Janela principal do app
class MainWindow(QMainWindow):


    def abrir_arquivo(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Audio (*.wav)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filename = dialog.selectedFiles()

            caminho = filename[0]


            file = arquivo()

            file.tratar_wav(caminho)
            

            self.abrir_janela_arquivo(file)

            

    def abrir_janela_arquivo(self, file):
        self.janela = figureWindow(file)


        self.janela.show()



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

janela = MainWindow()
janela.show()

app.exec()


'''
            
            '''