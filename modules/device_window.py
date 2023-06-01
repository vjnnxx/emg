import time
import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox)

from modules.dialogo import salvoDialog


from database.db import (get_conn,create_config)

from modules.canvas import Canvas

#Janela de gráfico dos arquivos externos
class deviceWindow(QWidget):


    def index_changed(self, index):
        
        dispositivo_selecionado = index

        for x in range(len(self.devices)):
            if self.devices[x]['nome_dispositivo'] == index:
                dispositivo_selecionado = self.devices[x]['id']
                self.config.set_device = self.devices[x]['id']
                break
        
        self.selected = dispositivo_selecionado
        

    def selecionar_dispositivo(self):
        
        conn = get_conn()

        config = {'id': self.selected}

        config = json.dumps(config)

        data = ('input_device', config)

        create_config(conn, data)

        salvoDialog()

        print('Dispositivo escolhido: ' + self.selected)

        self.close()

            
    def __init__(self, devices, config):
        super().__init__()

        self.devices = devices
        self.config = config
        self.selected = None

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
        botaoAnalise.clicked.connect(self.selecionar_dispositivo)
        

      

        layout.addWidget(botaoAnalise)


        self.setLayout(layout)


   
