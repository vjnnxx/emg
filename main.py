import sys
import webbrowser

from PySide6.QtCore import (Qt)
from PySide6 import QtCore
from PySide6.QtGui import QFont, QAction, QIcon
from PySide6.QtWidgets import ( QApplication, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow, QStyledItemDelegate, QTableWidgetItem, QTableWidget)


from modules.deviceWindow import deviceWindow
from modules.listWindow import listWindow
from modules.pessoaForm import pessoaForm
from modules.pessoaWindow import pessoaWindow
from modules.alertDialog import alertDialog
from modules.editWindow import editWindow


from database.start_db import start
from database.db import (get_conn, select_all_pessoas, table_exists)

import sounddevice as sd


conn = get_conn()

#Verifica e cria as tabelas caso ainda não existam no banco
table_check = table_exists(conn)
table_check = table_check[0]


if table_check == 0:
    start() 



class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


#Janela principal do app
class MainWindow(QMainWindow):

    


    #Fecha todas as janelas após fechar a main
    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()


    def cadastrar(self):
            self.janela_cadastrar = pessoaForm()
            self.janela_cadastrar.show()


    def create_callback_abrir(self, info):
        def button_clicked():
            try:
                self.janela_expandida = pessoaWindow(info)
                self.janela_expandida.show()
            except Exception as e:
                alertDialog('Ops, ocorreu um erro!')
                print(e)
        return button_clicked
    
    def create_callback_editar(self, info):
        def button_clicked():
            try:
                self.janela_editar = editWindow(info)
                self.janela_editar.show()
            except Exception as e:
                alertDialog('Ops, ocorreu um erro!')
                print(e)
        return button_clicked


    def abrir_janela_analises(self):
        self.janela_analises = listWindow()
        self.janela_analises.setGeometry(500, 300, 500, 500)
        self.janela_analises.show()
        

    def selecionar_dispositivo(self, devices):
       

        self.device_window = deviceWindow(devices)
        self.device_window.setGeometry(200, 200, 400, 300)

        self.device_window.show()

    def abrir_sobre(self):
        webbrowser.open('https://github.com/vjnnxx/emg')


    def atualizar_tabela(self):

        conn = get_conn()
        
        pessoas = select_all_pessoas(conn)
        linhas = len(pessoas)
        colunas = 3
        

        self.tabela.setRowCount(linhas)
        self.tabela.setColumnCount(colunas+2)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Nascimento", "", ""])

        #self.tabela.resize(300, 300)

        ids = []

        for item in pessoas:
            ids.append(item[0])

        for x in range(linhas):
            self.tabela.setItemDelegateForRow(x, self.delegate)
            for j in range(colunas):
                self.tabela.setItem(x, j, QTableWidgetItem(str(pessoas[x][j])))
            
            callback_abrir = self.create_callback_abrir(ids[x])

            btnAbrir = QPushButton(self.tabela)

            btnAbrir.clicked.connect(callback_abrir)
            btnAbrir.setText("Expandir")

            callback_editar = self.create_callback_editar(ids[x])

            btnEditar = QPushButton(self.tabela)
            btnEditar.clicked.connect(callback_editar)
            btnEditar.setText("Editar")

            self.tabela.setCellWidget(x, 3, btnAbrir)

            self.tabela.setCellWidget(x, 4, btnEditar)





    def __init__(self):
        super().__init__()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('EMG')

        self.setWindowIcon(QIcon('./sound-wave.ico'))

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


        about_menu = menu.addMenu('Sobre') 

        about_action = QAction('Sobre o projeto', self)
        about_menu.addAction(about_action)
        about_action.triggered.connect(self.abrir_sobre)

        #help_menu = menu.addMenu('Ajuda')
        
        

        layout_tabela = QVBoxLayout()

        self.setWindowTitle("EMG")
        self.resize(600, 500)
        self.setWindowIcon(QIcon('./sound-wave.ico'))

        title_font = QFont()
        title_font.setPixelSize(45)

        self.label = QLabel("Pessoas cadastradas")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(title_font)
        layout_tabela.addWidget(self.label)

        layout_horizontal = QHBoxLayout()   

        #Aqui

        #cria tabela 
        self.tabela = QTableWidget()
        

        self.delegate = ReadOnlyDelegate(self.tabela)
        
        self.atualizar_tabela()

        #Aqui
        
        #Criando fonte e aplicando configurações
        font = QFont()
        font.setPixelSize(30)

        self.tabela.resizeColumnsToContents()
        

        layout_tabela.addWidget(self.tabela)

        button = QPushButton('Cadastrar Nova Pessoa')
        button.setFont(font)
        button.clicked.connect(self.cadastrar)

        botao_atualizar = QPushButton('Atualizar tabela')
        botao_atualizar.clicked.connect(self.atualizar_tabela)

        layout_tabela.addWidget(button)
        layout_tabela.addWidget(botao_atualizar)

        layout_horizontal.addLayout(layout_tabela)

        base = QWidget()
        base.setLayout(layout_horizontal)

        self.setCentralWidget(base)

        self.setFixedSize(self.size())



app = QApplication(sys.argv)


janela = MainWindow()

janela.show()

sys.exit(app.exec())


