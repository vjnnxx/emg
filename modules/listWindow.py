
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QStyledItemDelegate)
from PySide6.QtGui import (QFont)

from modules.dialogo import customDialog
from modules.analysisWindow import analysisWindow

from database.db import *

#Ativa evento que impede edição da tabela
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        #print('evento createEditor disparado')
        return

#Janela de listagem de itens salvos no banco
class listWindow(QWidget):

    def voltar(self):
        self.close()


    def create_callback(self, info):
        def button_clicked():
            self.janela_analise = analysisWindow(info)
            self.janela_analise.show()
        return button_clicked
    
    

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setWindowTitle("Arquivos Salvos")
        self.resize(900, 500)

        self.label = QLabel("Lista de análises")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     

        conn = get_conn()

        analises = select_all_wav_data(conn)

        #print(analises)
        
        #print(analises[1][2])

        
        linhas = len(analises)
        colunas = 6

        #cria tabela 
        self.tabela = QTableWidget()

        delegate = ReadOnlyDelegate(self.tabela)
        
        

        self.tabela.setRowCount(linhas)
        self.tabela.setColumnCount(colunas+1)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Data","Duracao", "Caminho imagem", "Caminho Audio", "-"])
        
        

        ids = []

        for item in analises:
            ids.append(item[0])

        buttons = []

        


        for x in range(linhas):
            self.tabela.setItemDelegateForRow(x, delegate)
            for j in range(colunas):
                self.tabela.setItem(x, j, QTableWidgetItem(str(analises[x][j])))
            

            btn = QPushButton(self.tabela)


            callback = self.create_callback(ids[x])

            btn.clicked.connect(callback)
            btn.setText("Abrir")

            
            self.tabela.setCellWidget(x, 6, btn)

        


        self.tabela.resizeColumnsToContents()
        
        #self.tabela.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger)

        layout.addWidget(self.tabela)

        #Criando fonte e aplicando configurações
        font = QFont()
        font.setPixelSize(90)

        button = QPushButton('Voltar')
        button.setFont(font)
        button.clicked.connect(self.voltar)
        
        layout.addWidget(button)
        

        self.setLayout(layout)

        self.setFixedSize(self.size())


    
