from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QStyledItemDelegate)
from PySide6.QtGui import (QFont, QIcon)

import os

from modules.analysisWindow import analysisWindow
from modules.alertDialog import alertDialog
from modules.confirmDialog import confirmDialog
from modules.dialogo import customDialog

from database.db import *

#Ativa evento que impede edição da tabela
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return

#Janela de listagem de itens salvos no banco
class listWindow(QWidget):

    def voltar(self):
        self.close()

    def excluir_registro(self, id):

        
        dialog = confirmDialog()

        if dialog.exec_():
            #Excluir arquivos relacionados

            conn = get_conn()

            registro = select_wav_data(conn, id)

            caminho_imagem = registro[2]
            caminho_audio = registro[3]


            if os.path.isfile(caminho_imagem):
                os.remove(caminho_imagem)
            else:
                print("Erro, arquivo não encontrado.")

            audio_check = caminho_audio.startswith('./audio')

            #Exclui arquivo de áudio caso tenha sido gravado pelo sistema
            if audio_check: #transformar em função mais tarde
                if os.path.isfile(caminho_audio):
                    os.remove(caminho_audio)
                else:
                    print("Erro, arquivo não encontrado.")
            
            try:

                self.voltar()
                delete_wav_data(conn=conn, id=id)
                print("Registro excluído com sucesso!")
                customDialog("Registro excluído com sucesso! Por favor reabra a janela.")
 
            except Exception as e:
                print(e)
            conn.close()
            print('Confirmado')

        else:
            print('Melhor não!')


    def create_callback_abrir(self, info):
        def button_clicked():
            try:
                self.janela_analise = analysisWindow(info)
                self.janela_analise.show()
            except Exception as e:
                alertDialog('Arquivo de áudio não encontrado!')
                print(e)
        return button_clicked
    

    def create_callback_delete(self, info):
        def button_clicked():
            try:
                self.excluir_registro(info)
            except Exception as e:
                alertDialog('Algo deu errado!')
                print(e)
        return button_clicked
    

    
    

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setWindowTitle("Arquivos Salvos")
        self.resize(1000, 500)
        self.setWindowIcon(QIcon('./sound-wave.ico'))

        self.label = QLabel("Lista de análises")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     

        conn = get_conn()

        analises = select_all_wav_data(conn)

        
        linhas = len(analises)
        colunas = 6

        #cria tabela 
        self.tabela = QTableWidget()

        delegate = ReadOnlyDelegate(self.tabela)
        
        

        self.tabela.setRowCount(linhas)
        self.tabela.setColumnCount(colunas+2)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Data","Duracao", "Caminho imagem", "Caminho Audio", "-", "x"])
        
        

        ids = []

        for item in analises:
            ids.append(item[0])

        buttons = []

        


        for x in range(linhas):
            self.tabela.setItemDelegateForRow(x, delegate)
            for j in range(colunas):
                self.tabela.setItem(x, j, QTableWidgetItem(str(analises[x][j])))
            
            callback_abrir = self.create_callback_abrir(ids[x])

            btnAbrir = QPushButton(self.tabela)

            btnAbrir.clicked.connect(callback_abrir)
            btnAbrir.setText("Abrir")

            callback_delete = self.create_callback_delete(ids[x])

            btnDelete = QPushButton(self.tabela)
            btnDelete.clicked.connect(callback_delete)
            btnDelete.setText('Excluir')



            
            self.tabela.setCellWidget(x, 6, btnAbrir)

            self.tabela.setCellWidget(x, 7, btnDelete)

        


        self.tabela.resizeColumnsToContents()
        
        #self.tabela.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger)

        layout.addWidget(self.tabela)

        #Criando fonte e aplicando configurações
        font = QFont()
        font.setPixelSize(60)

        button = QPushButton('Voltar')
        button.setFont(font)
        button.clicked.connect(self.voltar)
        
        layout.addWidget(button)
        

        self.setLayout(layout)

        self.setFixedSize(self.size())


    
