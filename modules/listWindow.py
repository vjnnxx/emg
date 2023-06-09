import time


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem)

from modules.dialogo import salvoDialog

from database.db import *

#Janela de gráfico dos arquivos externos
class listWindow(QWidget):


            
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
        
        print(analises[1][2])

        
        linhas = len(analises)
        colunas = 6

        #cria tabela 
        self.tabela = QTableWidget()
        self.tabela.setRowCount(linhas)
        self.tabela.setColumnCount(colunas+1)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Data","Duracao", "Caminho imagem", "Caminho Audio", "Abrir"])
        


        for x in range(linhas):
            for j in range(colunas):
                self.tabela.setItem(x, j, QTableWidgetItem(str(analises[x][j])))
            self.tabela.setItem(x, 6, QTableWidgetItem("Botão pra abrir detalhes"))

        self.tabela.resizeColumnsToContents()
        #self.tabela.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger)

        layout.addWidget(self.tabela)

        print(len(analises))
        

        self.setLayout(layout)

        self.setFixedSize(self.size())


    
