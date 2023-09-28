import shutil
import os
import random

from PySide6.QtCore import (Qt, QTimer, QDateTime)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,QLabel, QPushButton, QLineEdit, QFileDialog)


from scipy.signal import find_peaks
from modules.dialogo import customDialog


from modules.canvas import Canvas


def random_string():
    
 
    random_string = ''
    
    for _ in range(16):
        # Considering only upper and lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))
    
    random_string += '.png'

    return random_string


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
        
        picos, _ = find_peaks(self.buffer, self.threshold)

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

            
    def __init__(self, buffer_quadrado, tempo):
        super().__init__()


        self.buffer = buffer_quadrado

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

        
        
        picos, _ = find_peaks(self.buffer, self.threshold)

        self.canva.ax.plot(self.buffer)
        
        self.canva.ax.plot(picos, self.buffer[picos], "x")




        layout_canva.addWidget(self.canva)

        layout_horizontal.addLayout(layout_canva)


        layout_inputs = QVBoxLayout()

        self.number_input = QLineEdit() 
        #self.number_input.setValidator(QDoubleValidator(0.00, 3 ,2))
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


    
        


