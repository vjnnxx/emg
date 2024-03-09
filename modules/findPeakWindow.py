import shutil
import os
import numpy as np
import json

from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,QLabel, QPushButton, QLineEdit, QFileDialog)
from PySide6.QtGui import (QIcon)


from scipy.signal import find_peaks
from modules.dialogo import customDialog


from modules.canvas import Canvas
from modules.random_string import random_string


#Janela de gráfico dos arquivos externos
class findPeakWindow(QWidget):

    def atualizar_valor(self, text):
        
        try:
            self.threshold = float(text)
            
        except Exception as e:
            self.threshold = 5
            print(e)

    def atualizar_canva(self):
        
        

        self.number_input.setText(str(self.threshold))

        self.canva.ax.clear()
        
        picos, _ = find_peaks(self.buffer, self.threshold, distance=4410) #acha picos a cada 100 ms

        self.canva.ax.plot(self.buffer)
        
        self.canva.ax.plot(picos, self.buffer[picos], "x")

        self.canva.draw()

        self.limit_label.setText(str(self.threshold))

    
    def exportar_imagem(self):

        nome_arquivo = random_string()

        self.canva.print_figure(nome_arquivo)

        folderDialog = QFileDialog(self)
        folderDialog.setFileMode(QFileDialog.FileMode.Directory)
        folderDialog.setOption(QFileDialog.Option.ShowDirsOnly)
        folderDialog.setViewMode(QFileDialog.ViewMode.List)
        
        if folderDialog.exec():
            selected_dir = folderDialog.selectedFiles()

            path_destino = selected_dir[0]
            
            try:

                dest = shutil.copy(nome_arquivo, path_destino)

                os.remove(nome_arquivo)

                customDialog("Arquivo exportado para: " + dest)
            
            except Exception as e:
                print(e)

            
    def __init__(self, buffer_quadrado, tempo, registro):
        super().__init__()
        self.setWindowIcon(QIcon('./sound-wave.ico'))

        self.buffer = buffer_quadrado

        self.buffer = self.buffer/10000

        buffer_quadrado = self.buffer ** 2

        self.buffer = np.sqrt(buffer_quadrado)

        self.tempo = tempo
    
        self.threshold = 1
       

        self.setWindowTitle("Encontrar picos")

       
        layout_horizontal = QHBoxLayout()   

        layout_canva = QVBoxLayout()

        self.label = QLabel("Encontrar picos")
        self.label.setAlignment(Qt.AlignCenter)
        layout_canva.addWidget(self.label)


        ''' Achar picos'''

        self.canva = Canvas()

        picos, _ = find_peaks(self.buffer, self.threshold, distance=4410) # picos a cada 100 ms

        self.canva.ax.plot(self.buffer)
        
        self.canva.ax.plot(picos, self.buffer[picos], "x")

        layout_canva.addWidget(self.canva)

        layout_horizontal.addLayout(layout_canva)

        self.number_input = QLineEdit() 
       
        self.number_input.textChanged.connect(self.atualizar_valor)
        

        botao = QPushButton('Encontrar')
        botao.clicked.connect(self.atualizar_canva)
        
        botaoExportar = QPushButton('Exportar imagem')
        botaoExportar.clicked.connect(self.exportar_imagem)

        self.limit_label = QLabel('-')


        form_layout = QFormLayout()

        form_layout.addRow("Valor", self.number_input)
        form_layout.addRow("", botao)
        form_layout.addRow("", botaoExportar)
        form_layout.addRow("Limite atual", self.limit_label)

        #layout_inputs.addWidget(number_input)

        #layout_inputs.addWidget(botao)

        layout_horizontal.addLayout(form_layout)
           
        

        self.setLayout(layout_horizontal)

        self.setFixedSize(self.size())


    
        


