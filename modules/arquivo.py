import numpy as np


class arquivo:

    def __init__(self, path='', wavedata='', sampleRate='', audioBuffer='',):
        self.path = path
        self.wavedata = wavedata
        self.sampleRate = sampleRate
        self.audioBuffer = audioBuffer

    def plot_wav(self):

        #extrai o nome do path
        name = self.path.split('/')
        name = name[-1]

        duration = len(self.audioBuffer)/self.sampleRate

        time = np.arange(0,duration,1/self.sampleRate) #time vector

        
        '''
        fig = plt.figure()

        plt.plot(time,self.audioBuffer/10000)
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude [V]')
        plt.title(name)
        plt.show()
        '''

       

    def debug(self):
        print(self.path, self.wavedata, self.sampleRate, self.audioBuffer)