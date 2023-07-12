import time


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QStyledItemDelegate)

from modules.dialogo import salvoDialog

from database.db import *

#Ativa evento que impede edição da tabela
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        #print('evento createEditor disparado')
        return

#Janela de listagem de itens salvos no banco
class listWindow(QWidget):
    
    def abrirAnalise(self, x):
        print(x)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setWindowTitle("Arquivos Salvos")
        self.resize(750, 500)

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
        
        
        

        for x in range(linhas):
            self.tabela.setItemDelegateForRow(x, delegate)
            for j in range(colunas):
                self.tabela.setItemDelegateForColumn(1, delegate)
                self.tabela.setItem(x, j, QTableWidgetItem(str(analises[x][j])))
            #self.tabela.setItem(x, 6, QTableWidgetItem("Botão pra abrir detalhes"))

            btn = QPushButton(self.tabela)

            btn.clicked.connect(lambda:self.abrirAnalise(self.tabela.item(x,0).text())) ###resolver
            btn.setText('Abrir')
            self.tabela.setCellWidget(x, 6, btn)

        self.tabela.resizeColumnsToContents()
        
        #self.tabela.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger)

        layout.addWidget(self.tabela)
        

        self.setLayout(layout)

        self.setFixedSize(self.size())


    
