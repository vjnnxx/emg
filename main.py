from qdarktheme import load_stylesheet
from PySide6.QtCore import (Qt)
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import ( 
    QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QMainWindow, QFileDialog, QLineEdit, QDialog, QDialogButtonBox)

from modules.arquivo import arquivo

from modules.signalWindow import signalWindow

import numpy as np

import queue
import sounddevice as sd

from modules.figureWindow import figureWindow

import matplotlib

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 
from matplotlib.animation import FuncAnimation






def printar():
    print('Botão foi clicado!')





#Janela principal do app
class MainWindow(QMainWindow):


    #Abre janela do windows para selecionar arquivos .wav
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

    def abrir_janela_sinal(self):
        self.janela = signalWindow()

        self.janela.show()


    def gravar_sinal(self):
        print('Gravar sinal')


    def rodar_grafico(self, layout):
        worker = Worker(layout)
        self.threadpool.start(worker)




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
        self.label = QLabel('Bem Vindo!')
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        botaoAbrir = QPushButton('Abrir arquivo')
        botaoAbrir.setFont(font)
        botaoAbrir.clicked.connect(self.abrir_arquivo)
        layout.addWidget(botaoAbrir)

        botaoGravar = QPushButton('Gravar Sinal')
        botaoGravar.setFont(font)
        botaoGravar.clicked.connect(self.abrir_janela_sinal)

        layout.addWidget(botaoGravar)

        #canva = Canvas()

        #layout.addWidget(canva)


        ''' DAQUI PRA BAIXO É BARRA'''
        
        #self.rodar_grafico(layout)



        base.setLayout(layout)
        self.setCentralWidget(base)



app = QApplication()
app.setStyleSheet(load_stylesheet())

janela = MainWindow()
janela.show()

app.exec()

