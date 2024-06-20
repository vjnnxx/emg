import os
import shutil

from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog)
from PySide6.QtGui import (QIcon)

from modules.findPeakWindow import findPeakWindow
from modules.rootMeanWindow import rootMeanWindow
from modules.dialogo import customDialog
from modules.confirmDialog import confirmDialog
from modules.arquivo import arquivo
from database.db import *

import numpy as np
from modules.canvas import Canvas

#Janela de gráfico dos arquivos externos
class analysisWindow(QWidget):

    def fecharJanela(self):
        self.close()
    
    def encontrar_picos(self, buffer, tempo, registro):
        if(buffer.ndim > 1):
            buffer = buffer[:, 0]
        self.peakWindow = findPeakWindow(buffer, tempo, registro)
        self.peakWindow.show()

    def root_mean(self, buffer, tempo):
        if(buffer.ndim > 1):
            buffer = buffer[:, 0]

        self.root_mean_window = rootMeanWindow(buffer, tempo)

        self.root_mean_window.show()

    def exportar_imagem(self, path_origem):

        folderDialog = QFileDialog(self)
        folderDialog.setFileMode(QFileDialog.FileMode.Directory)
        folderDialog.setOption(QFileDialog.Option.ShowDirsOnly)
        folderDialog.setViewMode(QFileDialog.ViewMode.List)
        
        if folderDialog.exec():
            selected_dir = folderDialog.selectedFiles()

            path_destino = selected_dir[0]
            
            try:

                dest = shutil.copy(path_origem, path_destino)

                customDialog("Arquivo exportado para: " + dest)
            
            except Exception as e:
                print(e)
            
    def excluir_registro(self, id):

        
        dialog = confirmDialog()

        if dialog.exec_():
            #Excluir arquivos relacionados

            conn = get_conn()

            registro = select_wav_data(conn, self.wav_id)

            caminho_imagem = registro[2]
            caminho_audio = registro[3]


            if os.path.isfile(caminho_imagem):
                os.remove(caminho_imagem)
            else:
                print("Erro, arquivo não encontrado.")

            audio_check = caminho_audio.startswith('./audio')

            #Exclui arquivo de áudio caso tenha sido gravado pelo sistema
            if audio_check: #transformar em função mais tarde
                if os.path.isfile(caminho_audio):
                    os.remove(caminho_audio)
                else:
                    print("Erro, arquivo não encontrado.")
            
            try:

                self.fecharJanela()
                delete_wav_data(conn=conn, id=self.wav_id)
 
            except Exception as e:
                print(e)
            else:
                
                delete_analise(conn=conn, id=id)

                print("Análise excluída com sucesso!")
                customDialog("Análise excluído com sucesso!")
            conn.close()
            print('Confirmado')

        else:
            print('Melhor não!')


    def __init__(self, id):
        super().__init__()

        self.setWindowTitle("Registros Salvos")

        self.setWindowIcon(QIcon('./sound-wave.ico'))

        
        self.file = arquivo()
        
        conn = get_conn()
        
        #id passado para a janela é o de análise, por isso é preciso buscar o id_wav_data para gerar o gráfico
        wav_id = get_id_wav_data(conn, id)

        self.wav_id = wav_id[0]

        registro = select_wav_data(conn, self.wav_id)

        nome = registro[0]
        
        duracao = registro[1]

        caminho_imagem = registro[2]

        caminho_audio = registro[3]

        sampleRate = registro[4]

        print(caminho_audio)

        #array numpy de 0 até a duração ao passo de 1 divido pelo SR
        tempo = np.arange(0,duracao,1/sampleRate) 

        self.file.tratar_wav(caminho_audio)

        buffer = select_buffer_wav_data(conn, id)

        buffer = json.loads(buffer[0])

        buffer = np.array(buffer)

        buffer = buffer/10000

        '''Cálculo do RMS'''

        buffer_quadrado = buffer ** 2

        buffer = np.sqrt(buffer_quadrado)

        self.setWindowTitle("Arquivo expandido")

        layout = QVBoxLayout()

        string_label = f'{nome} #ID: {id}'

        self.label = QLabel(string_label)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)     
        

        canva = Canvas()
        canva.ax.set_title(self.file.nome_arquivo)
        canva.ax.set_xlabel('Tempo [s]')
        canva.ax.set_ylim(-4,4)
        canva.ax.set_ylabel('Amplitude [Hz]')

        canva.ax.plot(self.file.tempo, self.file.audioBuffer/10000)

        layout.addWidget(canva)

        botaoRMS = QPushButton('Calcular RMS')
        botaoRMS.clicked.connect(lambda: self.root_mean(self.file.audioBuffer/10000,tempo))


        botaoPeaks = QPushButton('Achar Picos')
        botaoPeaks.clicked.connect(lambda: self.encontrar_picos(self.file.audioBuffer,tempo,registro))
        
        botaoExportar = QPushButton('Exportar imagem')
        botaoExportar.clicked.connect(lambda: self.exportar_imagem(caminho_imagem))

        botaoDelete = QPushButton('Excluir Registro')
        botaoDelete.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        botaoDelete.clicked.connect(lambda: self.excluir_registro(id))

        layout.addWidget(botaoRMS)
        layout.addWidget(botaoPeaks)
        layout.addWidget(botaoExportar)
        layout.addWidget(botaoDelete)

        self.setLayout(layout)

        self.setFixedSize(self.size())


    

        


