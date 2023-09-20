import sys

import json
from qdarktheme import load_stylesheet
from PySide6.QtCore import (Qt)
from PySide6 import QtCore
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import ( QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QMainWindow, QFileDialog)


from modules.signalWindow import signalWindow
from modules.figureWindow import figureWindow
from modules.deviceWindow import deviceWindow
from modules.listWindow import listWindow


from database.start_db import start
from database.db import (select_config_input_device, get_conn,create_tables, table_exists)

import sounddevice as sd


conn = get_conn()

#Verifica e cria as tabelas caso ainda não existam no banco
table_check = table_exists(conn)
table_check = table_check[0]

if table_check == 0:
    start() 


#Janela principal do app
class MainWindow(QMainWindow):


    #Fecha todas as janelas após fechar a main
    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()


    #Abre janela do windows para selecionar arquivos .wav
    def abrir_arquivo(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Audio (*.wav)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filename = dialog.selectedFiles()

            caminho = filename[0]
            

            self.abrir_janela_arquivo(caminho)




    def abrir_janela_arquivo(self, caminho):
        self.janela_arquivo = figureWindow(caminho)


        self.janela_arquivo.show()

    def abrir_janela_sinal(self):

        input_settings = select_config_input_device(conn)

        device = json.loads(input_settings[2])

        self.signal = signalWindow(device["id"])

        
        self.signal.show()

    def abrir_janela_analises(self):
        self.janela_analises = listWindow()

        self.janela_analises.setGeometry(1000, 50, 500, 500)
        #stack.addWidget(janela_analises)
        #stack.setCurrentIndex(stack.currentIndex()+1)
        self.janela_analises.show()
        

    def selecionar_dispositivo(self, devices):
       

        self.device_window = deviceWindow(devices)
        self.device_window.setGeometry(200, 200, 400, 300)

        self.device_window.show()

    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('EMG')

        base = QWidget()
        layout = QVBoxLayout()

        #Criando barra de menu
        

        menu = self.menuBar()


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
        

        #Cria botão para listar análises salvas

        botaoAnalises = QPushButton('Análises')
        botaoAnalises.setFont(font)
        botaoAnalises.clicked.connect(self.abrir_janela_analises)
        layout.addWidget(botaoAnalises)

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

        self.setFixedSize(self.size())



app = QApplication(sys.argv)
app.setStyleSheet(load_stylesheet())


janela = MainWindow()

janela.show()

sys.exit(app.exec())


