import numpy as np


class arquivo:

    def __init__(self, path='', wavedata='', sampleRate='', audioBuffer='',):
        self.path = path #arquivo externo
        self.wavedata = wavedata
        self.sampleRate = sampleRate
        self.audioBuffer = audioBuffer
        self.audiofile_path = ''
        self.imagefile_path = ''

    def plot_wav(self):

        #extrai o nome do path
        name = self.path.split('/')
        name = name[-1]

        duration = len(self.audioBuffer)/self.sampleRate

        time = np.arange(0,duration,1/self.sampleRate) #time vector


    def set_audiofile_path(self, path):
        self.audiofile_path = path
    
    def set_imagefile_path(self, path):
        self.imagefile_path = path


    def get_audiofile_path(self):
        return self.audiofile_path
    
    def get_imagefile_path(self):
        return self.imagefile_path
       

    def debug(self):
        print(self.path, self.wavedata, self.sampleRate, self.audioBuffer)