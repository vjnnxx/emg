import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import scipy.io
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt



#teste do botao de gravar

import queue
import sounddevice as sd
from matplotlib.animation import FuncAnimation


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

#Botão que abre arquivo wav e gera gráfico em uma nova janela
def browseFiles():


        try:
    
            filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", 
                filetypes = (("Wav files", '*.wav'),)
            )
            
            # Change label contents
            label_file_explorer.configure(text="Arquivo Aberto: "+filename)



            newWindow = Toplevel()

            newWindow.title('Gráfico')

            newWindow.geometry("900x600")

            newWindow.resizable(0,0)    

            #extraindo o nome do caminho

            name = filename.split('/')
            name = name[-1]

            file = arquivo()

            file.path = filename

            dataset_path = os.path.join(file.path) 
            file.wavedata = os.path.join(dataset_path)
        
            file.sampleRate, file.audioBuffer = scipy.io.wavfile.read(file.wavedata)

            duracao = len(file.audioBuffer)/file.sampleRate


            tempo = np.arange(0,duracao,1/file.sampleRate)
            
            fig = plt.figure(figsize=(5,5), dpi=100)

            a = fig.add_subplot(111)

            a.plot(tempo, file.audioBuffer/10000)

            plt.xlabel('Tempo [s]')
            plt.ylabel('Amplitude [Hz]')
            plt.title(name)

            canvas = FigureCanvasTkAgg(fig, newWindow)
            canvas.draw()
            canvas.get_tk_widget().grid(column=1, row=0)

            button_save = Button(newWindow, text = "Salvar", command = saveFile)

            button_analise = Button(newWindow, text= "Análise", command= analiseFile)

            button_save.grid(row=1)
            button_analise.grid(column=1, row=1)

        except:
            print('opa')        


def saveFile():
    print("Salvar arquivo")


def analiseFile():
    print("Analisar arquivo")

        
   
def showFigures():
     
     newWindow = Toplevel()

     newWindow.title('Nova janela')

     newWindow.geometry("500x500")

     newWindow.resizable(0,0)

     Label(newWindow, text= "Janela aberta com o botão").pack()


def recordAudio():


    newWindow = Toplevel()

    newWindow.title('Gráfico')

    newWindow.geometry("900x600")

    newWindow.resizable(0,0)    


    print('Botão para gravar audio')
    device = 0 # id of the audio device by default
    window = 1000 # window for the data
    downsample = 4 # how much samples to drop (inicialmente era 1)
    channels = [1] # a list of audio channels
    interval = 30 # this is update interval in miliseconds for plot

    # lets make a queue
    q = queue.Queue()
    
    device_info =  sd.query_devices(device, 'input')
    samplerate = device_info['default_samplerate']
    length  = int(window*samplerate/(1000*downsample))

   
    print("Sample Rate: ", samplerate)

    

    # Now we require a variable to hold the samples 

    plotdata =  np.zeros((length,len(channels)))
    # Lets look at the shape of this plotdata 
    print("plotdata shape: ", plotdata.shape)
    # So its vector of length 44100
    # Or we can also say that its a matrix of rows 44100 and cols 1

    # next is to make fig and axis of matplotlib plt
    fig,ax = plt.subplots(figsize=(8,4))

    # lets set the title
    ax.set_title("Entrada de áudio")

    # Make a matplotlib.lines.Line2D plot item of color green
    # R,G,B = 0,1,0.29

    lines = ax.plot(plotdata,color = (0,1,0.29))

    # We will use an audio call back function to put the data in queue

    def audio_callback(indata,frames,time,status):
        q.put(indata[::downsample,[0]])

    # now we will use an another function 
    # It will take frame of audio samples from the queue and update
    # to the lines

    def update_plot(frame):
        nonlocal plotdata
        while True:
            try: 
                data = q.get_nowait()
            except queue.Empty:
                break
            shift = len(data)
            plotdata = np.roll(plotdata, -shift,axis = 0)
            # Elements that roll beyond the last position are 
            # re-introduced 
            plotdata[-shift:,:] = data
            
        for column, line in enumerate(lines):
            line.set_ydata(plotdata[:,column])
        return lines
    ax.set_facecolor((0,0,0))
    # Lets add the grid
    #ax.set_yticks([1])
    ax.yaxis.grid(True)

    """ INPUT FROM MIC """

    stream  = sd.InputStream( device = device, channels = max(channels), samplerate = samplerate, callback  = audio_callback)


    """ OUTPUT """		


    plt.ylim(top=1)
    
    canvas = FigureCanvasTkAgg(fig, newWindow)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=0)
    ani  = FuncAnimation(fig,update_plot, interval=interval,blit=True)
    

    plt.ylabel("Amplitude")
    
    with stream:
        plt.show()


root = Tk()

#Configurações do menu superior
menu = Menu(root)

root.config(menu=menu)

menuArquivo = Menu(menu)
menu.add_cascade(label="Arquivo", menu=menuArquivo)
menuArquivo.add_command(label="Abrir")

menuSalvar = Menu(menu)
menu.add_cascade(label="Salvar", menu=menuSalvar)
menuSalvar.add_command(label="Salvar como...")

menuAnalises = Menu(menu)
menu.add_cascade(label="Análises", menu=menuAnalises)
menuAnalises.add_command(label="Nova análise")
menuAnalises.add_command(label="Gerenciar análises")

menuConfig = Menu(menu)
menu.add_cascade(label="Configurações", menu=menuConfig)
menuConfig.add_command(label="Entrada")
menuConfig.add_command(label="Gráfico")

root.maxsize(900,600)

root.geometry("900x600")

root.resizable(0,0)

root.title("EMG")

mainframe = ttk.Frame(root)

label_file_explorer = Label(root,text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")

button_explore = Button(root, text = "Abrir arquivo", command = browseFiles)

button_show = Button(root, text='Exibir figuras salvas', command= showFigures)

button_record = Button(root, text='Gravar áudio', command=recordAudio)

button_exit = Button(root, text="Sair", command=exit)




label_file_explorer.grid(column = 0, row = 1)
  
button_explore.grid(column = 0, row = 2)
  
button_show.grid(column=0, row=3)

button_record.grid(column=0, row=4)

button_exit.grid(column = 0,row = 5)


root.mainloop()