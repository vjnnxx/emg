from PySide6.QtCore import (QThreadPool)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,QLabel, QPushButton, QLineEdit, QFileDialog, QProgressBar)
from PySide6.QtGui import (QIcon)


from modules.canvas import Canvas
import numpy as np
from modules.random_string import random_string
from modules.dialogo import customDialog
import math
import os
import shutil

#Janela de gráfico dos arquivos externos
class rootMeanWindow(QWidget):

    def atualizar_valor(self, text):
        
        try:
            self.janela = float(text) * 44.1

            self.janela = int(self.janela)
        except Exception as e:
            self.janela = 4410 # 100 ms
            print(e)

    def rodar_att(self):
        self.thread_manager.start(self.atualizar_canva)
        

        

    def atualizar_canva(self):
        
        #Colocar tudo numa thread // fazer barra de load


        #44100 posições do array == 1 segundo ---> 44100 / 10 === 100 ms

        janela = int(self.janela)

        self.media_movel = []

        maximo = len(self.buffer - janela + 1)

        self.progressBar.setMaximum(maximo)

        for x in range(len(self.buffer - janela + 1)):
            self.media_movel.append(np.mean(self.buffer[x:x+janela]))

            #self.progressBar.setValue(x + 1)


        self.canva.ax.clear()
        
        self.canva.ax.plot(self.tempo, self.buffer)

        self.canva.ax.plot(self.tempo, self.media_movel)
        
        

        self.canva.draw()

        self.limit_label.setText(str(self.janela/44.1))

    def exportar_imagem(self):


        folderDialog = QFileDialog(self)
        folderDialog.setFileMode(QFileDialog.FileMode.Directory)
        folderDialog.setOption(QFileDialog.Option.ShowDirsOnly)
        folderDialog.setViewMode(QFileDialog.ViewMode.List)
        
        if folderDialog.exec():
            

            selected_dir = folderDialog.selectedFiles()

            path_destino = selected_dir[0]
            
            try:

                nome_arquivo = random_string()
                self.canva.print_figure(nome_arquivo)

                dest = shutil.copy(nome_arquivo, path_destino)

                os.remove(nome_arquivo)

                customDialog("Arquivo exportado para: " + dest)
            
            except Exception as e:
                print(e)
    
            
    def __init__(self, buffer, tempo):
        super().__init__()

        self.setWindowIcon(QIcon('./sound-wave.ico'))

        buffer_quadrado = buffer ** 2

        buffer = np.sqrt(buffer_quadrado)


        self.buffer = buffer

        self.tempo = tempo

        self.tamanho_buffer = np.size(self.buffer)

        self.media_movel = []

        self.thread_manager = QThreadPool()

        self.progressBar = QProgressBar()

        self.progressBar.setMinimum(0)
        

        self.janela = math.ceil(44100 / 10) #100 ms

        self.setWindowTitle("RMS")

       
        layout_horizontal = QHBoxLayout()   

        layout_canva = QVBoxLayout()

        self.label = QLabel("RMS")

        layout_canva.addWidget(self.label)

        layout_canva = QVBoxLayout()


        self.canva = Canvas()

        self.canva.ax.plot(self.tempo, self.buffer)

        layout_canva.addWidget(self.canva)

        layout_horizontal.addLayout(layout_canva)

        self.setLayout(layout_horizontal)

        self.number_input = QLineEdit() 
        self.number_input.textChanged.connect(self.atualizar_valor)
        

        botao = QPushButton('Calcular')
        botao.clicked.connect(self.rodar_att) 
        
        botaoExportar = QPushButton('Exportar imagem')
        botaoExportar.clicked.connect(self.exportar_imagem) 

        botaoTeste = QPushButton('Teste')

        self.limit_label = QLabel('-')

        form_layout = QFormLayout()

        form_layout.addRow("Janela", self.number_input)
        form_layout.addRow("", botao)
        form_layout.addRow("", botaoExportar)
        form_layout.addRow("Progresso:", self.progressBar)
        form_layout.addRow("Janela atual", self.limit_label)

        

        layout_horizontal.addLayout(form_layout)

       
        self.setFixedSize(self.size())


    
        


