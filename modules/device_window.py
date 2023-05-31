import time


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox)

from modules.dialogo import salvoDialog

from modules.canvas import Canvas

#Janela de gráfico dos arquivos externos
class deviceWindow(QWidget):


    def index_changed(self, index):
        
        for x in range(len(self.devices)):
            if self.devices[x]['nome_dispositivo'] == index:
                print(self.devices[x]['id'])
                self.config.set_device = self.devices[x]['id']
                break
            
            


        #
        #print("Index Changed", index)

            
    def __init__(self, devices, config):
        super().__init__()

        self.devices = devices
        self.config = config

        layout = QVBoxLayout()

        self.label = QLabel('Escolha um dos dispositivos disponíveis')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     

        combobox = QComboBox()
        combobox.currentTextChanged.connect(self.index_changed)

        layout.addWidget(combobox)

        #Adiciona itens com nomes dos dispositivos de entrada disponíveis
        for x in range(len(devices)):
            combobox.addItem(devices[x]['nome_dispositivo'])
        
      




        #fechar janela
        botaoAnalise = QPushButton('Selecionar')
        

      

        layout.addWidget(botaoAnalise)


        self.setLayout(layout)


   
