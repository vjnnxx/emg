from PySide6.QtCore import (Qt, QDate)
from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QDateEdit)
from PySide6.QtGui import (QIcon)

from datetime import datetime

from modules.dialogo import customDialog

from database.db import update_pessoa, get_conn, select_pessoa_by_id


#Janela de gráfico dos arquivos externos
class editWindow(QWidget):

    def change_name(self, nome):
        self.nome = nome

    def change_date(self, date):
        data_aux = date.toString()
        data_aux = datetime.strptime(data_aux, '%a %b %d %Y').strftime('%d-%m-%Y')
        self.data_nasc = data_aux

    def change_obs(self, obs):
        self.obs = obs

    def atualizar_pessoa(self):

        if(self.nome == '' or len(self.nome) < 4):
            print('Nome precisa ter no mínimo quatro caracteres!')
            return
        
        if(self.data_nasc == ''):
            print('Data de nascimento precisa ser preenchida!')
            return
        
        conn = get_conn()

        pessoa = (self.nome, self.data_nasc, self.obs, self.id)

        update_pessoa(conn, pessoa)

        customDialog('Informações atualizadas com sucesso!')

        self.close()
        
        

            
    def __init__(self, id):
        super().__init__()
        self.setWindowIcon(QIcon('./sound-wave.ico'))
        
        self.id = id

        conn = get_conn()

        pessoa = select_pessoa_by_id(conn, self.id)

        nome = pessoa[1]

        data_nasc = pessoa[2]

        obs = pessoa[3]
        

        self.setWindowTitle("Editar Informações")

        self.nome = nome
        self.data_nasc = data_nasc
        self.obs = obs

        layout = QFormLayout()

        self.label = QLabel("Editar Informações de {}".format(nome))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     

        input_nome = QLineEdit()
        input_nome.setText(nome)
        input_nome.textChanged.connect(self.change_name)

        input_data = QDateEdit()
       

        qdate = QDate.fromString(data_nasc, "dd-mm-yyyy")

        input_data.setDate(qdate)

        input_data.setCalendarPopup(True)

        input_data.dateChanged.connect(self.change_date)

        input_observacoes = QLineEdit()
        input_observacoes.setText(obs)
        input_observacoes.textChanged.connect(self.change_obs)

        botao_enviar = QPushButton('Enviar')
        botao_enviar.clicked.connect(self.atualizar_pessoa)

        layout.addRow("Nome", input_nome)
        layout.addRow("Data de nascimento", input_data)
        layout.addRow("Observações", input_observacoes)
        layout.addRow("", botao_enviar)
        
    

        self.setLayout(layout)

        self.setFixedSize(self.size())

        


