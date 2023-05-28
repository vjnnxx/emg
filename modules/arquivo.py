import numpy as np

import matplotlib.pyplot as plt
import os

import scipy.io
import scipy.io.wavfile

class arquivo:

    def __init__(self, path='', wavedata='', sampleRate='', audioBuffer='',):
        self.path = path #arquivo externo
        self.sampleRate = sampleRate
        self.audioBuffer = audioBuffer
        self.audiofile_path = ''
        self.imagefile_path = ''
        self.duracao_audio = ''
        self.tempo = ''
        self.nome_arquivo = ''


    def set_audiofile_path(self, path):
        self.audiofile_path = path
    
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
            
            
            #Transforma arquivo selecionado em um buffer de audio 
            self.sampleRate, self.audioBuffer = scipy.io.wavfile.read(self.path)

            duracao = len(self.audioBuffer)/self.sampleRate

            self.set_duracao(duracao)
            
            #array numpy de 0 até a duração ao passo de 1 divido pelo SR
            tempo = np.arange(0,duracao,1/self.sampleRate)

            self.set_tempo(tempo)

    def salvar_figura(self):

        if(self.audioBuffer == '' or self.tempo == ''):
            return 'Dados faltantes!'
        

        #Cria um diretório para guardar figuras caso ainda não exista
        try:
            os.makedirs('./figures')
        except:
            pass
        
        fig = plt.figure(figsize=(5,5), dpi=100)

        a = fig.add_subplot(111)

        a.plot(self.tempo, self.audioBuffer/10000)

        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude [Hz]')
        plt.title(self.nome_arquivo)

        my_path = './figures'
        name = self.nome_arquivo.split('.')
        my_file = name[0] + '.png'
            
        plt.savefig(os.path.join(my_path,my_file))
        
        plt.close()

        print('ok')

       

    def debug(self):
        print(self.path, self.wavedata, self.sampleRate, self.audioBuffer)