from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt


#Classe para guardar informações do arquivo .wav
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

        fig = plt.figure()

        plt.plot(time,self.audioBuffer)
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude')
        plt.title(name)
        plt.show()


       

    def debug(self):
        print(self.path, self.wavedata, self.sampleRate, self.audioBuffer)


def browseFiles():


    
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", 
            filetypes = (("Wav files", '*.wav'),)
        )
        
        # Change label contents
        label_file_explorer.configure(text="Arquivo Aberto: "+filename)

        file = arquivo()

        file.path = filename

        dataset_path = os.path.join(file.path) 
        file.wavedata = os.path.join(dataset_path)
    
        file.sampleRate, file.audioBuffer = scipy.io.wavfile.read(file.wavedata)

        file.plot_wav()
   
def showFigures():
    print('qualquer coisa')

root = Tk()

root.maxsize(900,600)

root.geometry("900x600")

root.resizable(0,0)

root.title("EMG")

mainframe = ttk.Frame(root)

label_file_explorer = Label(root,text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")

button_explore = Button(root, text = "Abrir arquivo", command = browseFiles)

button_show = Button(root, text='Exibir figuras salvas', command= showFigures)

button_exit = Button(root, text="Sair", command=exit)




label_file_explorer.grid(column = 0, row = 1)
  
button_explore.grid(column = 0, row = 2)
  
button_show.grid(column=0, row=3)

button_exit.grid(column = 0,row = 4)


root.mainloop()