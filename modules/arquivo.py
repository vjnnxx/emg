import numpy as np
import json 
import time
from pydub import AudioSegment
from pydub.playback import play

import soundfile as sf

from database.db import (create_wav_data, get_conn, select_last_wav_data_id , create_analise)

from datetime import date

import matplotlib.pyplot as plt
import os
import posixpath

import scipy.io
import scipy.io.wavfile


def get_file_extension(path):
    extension = path.split('/')
    extension = extension[-1]
    extension = extension.split('.')
    extension = extension[-1]

    return extension

#classe para converter np array em JSON
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class arquivo:

    def __init__(self, path='', sampleRate='', audioBuffer='',):
        self.path = path #arquivo externo
        self.sampleRate = sampleRate
        self.audioBuffer = audioBuffer
        self.imagefile_path = ''
        self.duracao_audio = ''
        self.tempo = ''
        self.nome_arquivo = ''


    
    def set_imagefile_path(self, path):
        self.imagefile_path = path


    def get_audiofile_path(self):
        return self.audiofile_path
    
    def get_imagefile_path(self):
        return self.imagefile_path
    
    def set_duracao(self, duracao):
        self.duracao_audio = duracao

    def set_tempo(self, tempo):
        self.tempo = tempo

    def set_nome_arquivo(self, nome):
        self.nome_arquivo = nome
    

    def tratar_wav(self, caminho):
            
            #Pegando guardando caminho do arquivo
            self.path = os.path.join(caminho)
            
            nome = self.path.split('/')
            nome = nome[-1]

            self.set_nome_arquivo(nome)

            not_wav = False

            if(get_file_extension(self.path) != 'wav'):
                not_wav = True
                data, samplerate = sf.read(self.path)
                file_name = nome.split('.')
                file_name = file_name[0] + '.wav'
                path = './audio/{}'.format(file_name)
                sf.write(path, data=data, samplerate=samplerate)
                print(samplerate)
                self.path = os.path.join(path)
                
            #Transforma arquivo selecionado em um buffer de audio 
            self.sampleRate, self.audioBuffer = scipy.io.wavfile.read(self.path)

            if(not_wav):
                self.audioBuffer = self.audioBuffer[:, 0]

            duracao = len(self.audioBuffer)/self.sampleRate

            self.set_duracao(duracao)
            
            #array numpy de 0 até a duração ao passo de 1 divido pelo SR
            tempo = np.arange(0,duracao,1/self.sampleRate)

            self.set_tempo(tempo)


    #Função para tratar os dados e salvar a figura
    def salvar_figura(self, id, nome):
        if(self.audioBuffer.size == 0):
            return 'Dados faltantes!'
        
        id_pessoa = id

        #Cria um diretório para guardar figuras caso ainda não exista
        try:
            os.makedirs('./figures')

            os.system("attrib +h figures")
        except:
            pass
        
        fig = plt.figure(figsize=(5,5), dpi=100)

        a = fig.add_subplot(111)

        a.plot(self.tempo, self.audioBuffer/10000) #adicionar y no grafico de picos


        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude [Hz]')
        plt.title(self.nome_arquivo)

        my_path = './figures'
        name = self.nome_arquivo.split('.')
        my_file = name[0] + '.png'


        self.set_imagefile_path(posixpath.join(my_path,my_file))

            
        plt.savefig(self.imagefile_path)
        
        plt.close()

        today = date.today()

        # dd/mm/YY
        data_atual = today.strftime("%d/%m/%Y")
        buffer_tratado = json.dumps(self.audioBuffer, cls=NumpyEncoder)

        caminho_audio = ''

        if self.path != '':
            caminho_audio = self.path

        data = (my_file, data_atual, self.duracao_audio, self.imagefile_path, caminho_audio, buffer_tratado, self.sampleRate)
        
        conn = get_conn()


        #criar análise depois de criar wav data e linkar id do wav data criado

        create_wav_data(conn=conn, wav_data = data)


        time.sleep(1)

        #get last wav data id

        last_id = select_last_wav_data_id(conn)

        last_id = last_id[0]

        analise = (nome, id_pessoa, last_id)

        create_analise(conn, analise)

        conn.close()


    