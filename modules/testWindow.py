from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout ,QLabel, QPushButton, QTableWidget, QTableWidgetItem, QStyledItemDelegate)
from PySide6.QtGui import (QFont, QIcon)

import os

from modules.analysisWindow import analysisWindow
from modules.alertDialog import alertDialog
from modules.pessoaForm import pessoaForm

from database.db import *

#Ativa evento que impede edição da tabela
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class testWindow(QWidget):

    def cadastrar(self):
        self.janela_cadastrar = pessoaForm()
        self.janela_cadastrar.show()


    def create_callback_abrir(self, info):
        def button_clicked():
            try:
                self.janela_analise = analysisWindow(info)
                self.janela_analise.show()
            except Exception as e:
                alertDialog('Arquivo de áudio não encontrado!')
                print(e)
        return button_clicked
    

    def __init__(self):
        super().__init__()

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

        conn = get_conn()

        pessoas = select_all_pessoas(conn)

        
        linhas = len(pessoas)
        colunas = 3

        #cria tabela 
        self.tabela = QTableWidget()

        delegate = ReadOnlyDelegate(self.tabela)
        
        

        self.tabela.setRowCount(linhas)
        self.tabela.setColumnCount(colunas+1)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Nascimento", "-"])

        self.tabela.resize(300, 300)
        
        

        ids = []

        for item in pessoas:
            ids.append(item[0])

        buttons = []

        


        for x in range(linhas):
            self.tabela.setItemDelegateForRow(x, delegate)
            for j in range(colunas):
                self.tabela.setItem(x, j, QTableWidgetItem(str(pessoas[x][j])))
            
            callback_abrir = self.create_callback_abrir(ids[x])

            btnAbrir = QPushButton(self.tabela)

            btnAbrir.clicked.connect(callback_abrir)
            btnAbrir.setText("Expandir")




            
            self.tabela.setCellWidget(x, 3, btnAbrir)

            #self.tabela.setCellWidget(x, 7, btnDelete)

        
        #Criando fonte e aplicando configurações
        font = QFont()
        font.setPixelSize(30)

        self.tabela.resizeColumnsToContents()
        
        #self.tabela.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger)

        layout_tabela.addWidget(self.tabela)

        button = QPushButton('Cadastrar Pessoa')
        button.setFont(font)
        button.clicked.connect(self.cadastrar)

        layout_tabela.addWidget(button)

        layout_horizontal.addLayout(layout_tabela)
              

        self.setLayout(layout_horizontal)

        self.setFixedSize(self.size())


    
