from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout ,QLabel, QPushButton, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QFileDialog)
from PySide6.QtGui import (QFont, QIcon)


from modules.alertDialog import alertDialog
from modules.newAnalysis import newAnalysis
from modules.analysisWindow import analysisWindow

from database.db import *

#Ativa evento que impede edição da tabela
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class pessoaWindow(QWidget):
    
    def atualizar_tabela(self):

        conn = get_conn()

        analises = get_analise_by_pessoa_id(conn, self.id)
        linhas = len(analises)
        colunas = 2

        self.tabela.setRowCount(linhas)
        self.tabela.setColumnCount(colunas+1)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Visualizar"])
        self.tabela.resize(300, 300)
        ids = []

        for item in analises:
            ids.append(item[0])

        for x in range(linhas):
            self.tabela.setItemDelegateForRow(x, self.delegate)
            for j in range(colunas):
                self.tabela.setItem(x, j, QTableWidgetItem(str(analises[x][j])))
            
            callback_abrir = self.create_callback_abrir(ids[x])

            btnAbrir = QPushButton(self.tabela)

            btnAbrir.clicked.connect(callback_abrir)
            btnAbrir.setText("Expandir")
            
            self.tabela.setCellWidget(x, 2, btnAbrir)
    


    def cadastrar(self):
        self.janela_nova_analise = newAnalysis(self.id)
        self.janela_nova_analise.show()


    def create_callback_abrir(self, info):
        def button_clicked():
            try:
                self.janela_analise = analysisWindow(info)
                self.janela_analise.show()
            except Exception as e:
                alertDialog('Arquivo de áudio não encontrado!')
                print(e)
        return button_clicked
    

    def __init__(self, id):
        super().__init__()
        self.id = id #PessoaID 

        conn = get_conn()
        pessoa = select_pessoa_by_id(conn, self.id)
        nome_completo = pessoa[1]
        primeiro_nome = nome_completo.split(" ")
        primeiro_nome = primeiro_nome[0]
        
        layout_tabela = QVBoxLayout()

        self.setWindowTitle("{}".format(nome_completo))
        self.resize(600, 500)
        self.setWindowIcon(QIcon('./sound-wave.ico'))

        title_font = QFont()
        title_font.setPixelSize(45)

        self.label = QLabel("Análises de {}".format(primeiro_nome))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(title_font)
        layout_tabela.addWidget(self.label)

        layout_horizontal = QHBoxLayout()   

        #cria tabela 
        self.tabela = QTableWidget()
        self.delegate = ReadOnlyDelegate(self.tabela)
        self.atualizar_tabela()
        
        #Criando fonte e aplicando configurações
        font = QFont()
        font.setPixelSize(30)

        self.tabela.resizeColumnsToContents()
        
        #self.tabela.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger)

        layout_tabela.addWidget(self.tabela)


        button = QPushButton('Nova Análise')
        button.setFont(font)
        button.clicked.connect(self.cadastrar)

        botao_atualizar = QPushButton('Atualizar Tabela')
        botao_atualizar.clicked.connect(self.atualizar_tabela)

        layout_tabela.addWidget(button)
        layout_tabela.addWidget(botao_atualizar)


        #Criar botão e tela para vizualizar informações

        layout_horizontal.addLayout(layout_tabela)


              

        self.setLayout(layout_horizontal)

        self.setFixedSize(self.size())


    