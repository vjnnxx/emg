import sys
from qdarktheme import load_stylesheet
from PySide6.QtCore import (Qt)
from PySide6 import QtCore
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import ( 
    QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QMainWindow, QFileDialog, QLineEdit, QDialog, QDialogButtonBox)


from modules.arquivo import arquivo

from modules.signalWindow import signalWindow
from modules.figureWindow import figureWindow
from modules.device_window import deviceWindow
from modules.config import config

import numpy as np

import queue
import sounddevice as sd

config = config()


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
        self.signal = signalWindow()

        
        self.signal.show()


    def gravar_sinal(self):
        print('Gravar sinal')


    def rodar_grafico(self, layout):
        print('rodando')
        #self.threadpool.start(worker)



    def selecionar_dispositivo(self, devices):
        #Fazer select com nomes de dispositivos de entrada em um dialog

        self.device_window = deviceWindow(devices, config)
        self.device_window.setWindowTitle("Selecionar dispositivo")
        self.device_window.setGeometry(200, 200, 400, 300)

        self.device_window.show()
        

        #print(devices)



    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        base = QWidget()
        layout = QVBoxLayout()


        #Criando barra de menu
        
        action = QAction('Ação', self)
        action.triggered.connect(printar)
        menu = self.menuBar()
        file_menu = menu.addMenu('Menu')
        file_menu.addAction(action)


        dispositivos = sd.query_devices()

        #Cria opção no menu superior para selecionar dispositivos de audio

        audio_menu = menu.addMenu('Dispositivo de áudio')

       

        input_devices = []


        for x in range(len(dispositivos)):
            if dispositivos[x]['max_input_channels'] > 0:
                action = { 'id': x, 'nome_dispositivo': dispositivos[x]['name']}
                input_devices.append(action)


        device_select_action = QAction('Selecionar dispositivo', self)
        audio_menu.addAction(device_select_action)
        device_select_action.triggered.connect(lambda:self.selecionar_dispositivo(input_devices))

        

        #Criando fonte e aplicando configurações
        font = QFont()
        font.setPixelSize(90)


        #Criando label
        self.label = QLabel('Bem Vindo!')
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
       

        base.setLayout(layout)
        self.setCentralWidget(base)



app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet())

janela = MainWindow()
janela.show()

sys.exit(app.exec())


