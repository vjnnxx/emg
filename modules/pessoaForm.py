from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFormLayout, QLineEdit, QCalendarWidget, QDateEdit)
from PySide6.QtGui import (QIcon)

from datetime import datetime

from modules.dialogo import customDialog

from database.db import create_pessoa, get_conn







#Janela de gráfico dos arquivos externos
class pessoaForm(QWidget):

    def change_name(self, nome):
        self.nome = nome

    def change_date(self, date):
        data_aux = date.toString()
        data_aux = datetime.strptime(data_aux, '%a %b %d %Y').strftime('%d-%m-%Y')
        self.data_nasc = data_aux

    def change_obs(self, obs):
        self.obs = obs

    def cadastrar_pessoa(self):

        if(self.nome == '' or len(self.nome) < 4):
            print('Nome precisa ter no mínimo quatro caracteres!')
            return
        
        if(self.data_nasc == ''):
            print('Data de nascimento precisa ser preenchida!')
            return
        
        conn = get_conn()

        pessoa = (self.nome, self.data_nasc, self.obs)

        create_pessoa(conn, pessoa)

        print('Ta cadastrado meu pit')

        
        

            
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./sound-wave.ico'))
        

        self.setWindowTitle("Formulário")

        self.nome = ''
        self.data_nasc = ''
        self.obs = ''

        layout = QFormLayout()

        self.label = QLabel("Formulário de cadastro")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     

        input_nome = QLineEdit()
        input_nome.textChanged.connect(self.change_name)

        input_data = QDateEdit()
        input_data.setCalendarPopup(True)
        input_data.dateChanged.connect(self.change_date)

        input_observacoes = QLineEdit()
        input_observacoes.textChanged.connect(self.change_obs)

        botao_enviar = QPushButton('Enviar')
        botao_enviar.clicked.connect(self.cadastrar_pessoa)

        layout.addRow("Nome", input_nome)
        layout.addRow("Data de nascimento", input_data)
        layout.addRow("Observações", input_observacoes)
        layout.addRow("", botao_enviar)
        
    

        self.setLayout(layout)

        self.setFixedSize(self.size())

        


