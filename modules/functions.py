from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import filedialog
from tkinter import messagebox as mb

import threading

import os 

import sys
sys.path.append('./modules')
from modules.arquivo import arquivo
from modules.player import player

import numpy as np

import tkinter as tk
import scipy.io
import scipy.io.wavfile
import time

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import wave
import queue
import sounddevice as sd
import pyaudio
from matplotlib.animation import FuncAnimation


#função que seleciona arquivo
def browseFiles():

        try:
    
            filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", 
                filetypes = (("Wav files", '*.wav'),)
            )

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
            #canvas.get_tk_widget().grid(column=1, row=0)
            canvas.get_tk_widget().pack()

            button_save = Button(newWindow, text = "Salvar", command= lambda: saveFile(filename))

            button_analise = Button(newWindow, text= "Análise", command= analiseFile)

            button_exit = Button(newWindow, text="Sair", command=newWindow.destroy)

            button_save.pack()
            button_analise.pack()
            button_exit.pack()

            plt.close()
        
        except Exception as e:
            print('Algo deu errado...')
            print(e)
            pass        

def saveFile(filename):
   
    try:
        os.makedirs('./figures')
    except:
        pass
    
    name = filename.split('/')
    name = name[-1]

    dataset_path = os.path.join(filename) 
    wavedata = os.path.join(dataset_path)
        
    sampleRate, audioBuffer = scipy.io.wavfile.read(wavedata)

    duracao = len(audioBuffer)/sampleRate


    tempo = np.arange(0,duracao,1/sampleRate)
            
    fig = plt.figure(figsize=(5,5), dpi=100)

    a = fig.add_subplot(111)

    a.plot(tempo, audioBuffer/10000)

    plt.xlabel('Tempo [s]')
    plt.ylabel('Amplitude [Hz]')
    plt.title(name)

    my_path = './figures'
    name = name.split('.')
    my_file = name[0] + '.png'
        
    plt.savefig(os.path.join(my_path,my_file))
    
    plt.close()

    print('ok')
    
def analiseFile():
    print("Analisar arquivo")

def showFigures():
     
     newWindow = Toplevel()

     newWindow.title('Nova janela')

     newWindow.geometry("500x500")

     newWindow.resizable(0,0)

     Label(newWindow, text= "Janela aberta com o botão").pack()

def recordAudio():

    plt.close()

    newWindow = Toplevel()

    newWindow.title('Live Audio')

    newWindow.geometry("900x500")

    newWindow.resizable(0,0)

    Label(newWindow, text= "Janela grafico live").grid()

    device = 0 # id of the audio device by default
    window = 1000 # window for the data
    downsample = 1 # how much samples to drop (inicialmente era 1)
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
    ani  = FuncAnimation(fig,update_plot, interval=interval,blit=True)
    canvas.draw()
    canvas.get_tk_widget().grid(column=0, row=1)


    thread1 = ''
    aux = '' 

    file = arquivo()

    button_start = Button(newWindow, text= "Iniciar", command=lambda: [run_thread(thread1,record,file)])
    button_pause = Button (newWindow, text= "Parar", command=lambda: [stop(True)])
    button_exit = Button(newWindow, text="Sair", command= lambda: [stop(False), newWindow.destroy()])

    button_start.grid(column=0, row=2)
    button_pause.grid(column=1, row=2)
    button_exit.grid(column=2, row=2)
    
    

    plt.ylabel("Amplitude")
    
    #figure = plt.figure()

    with stream:
      plt.show()

    
    vasco = file.get_audiofile_path()
    #print(vasco)



tocar = player() 


def record(file):
        
    
    #logica para gravar audio
        

    #root.event_generate("<<vasco>>", when="tail")



    tocar.switch_on(True)

    tocar.start_timer()

    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)


    frames = []
               

         
    print("Gravando áudio...")

    while tocar.get_on():
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    try:
        os.makedirs('./audio')
    except:
        pass


    #conta o número de arquivos na pasta audio para numerar os arquivos salvos
    lst = os.listdir('./audio') 
    number_files = len(lst)


    str_number = str(number_files)

    if(number_files > 10):
        str_number = str_number.zfill(3)
    else:
        str_number = str_number.zfill(3)

    novo_arquivo = './audio/audio' + str_number + '.wav' 

    sound_file = wave.open(novo_arquivo, 'wb')
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    #Guarda o caminho da arquivo de áudio em uma classe
    file.set_audiofile_path(novo_arquivo)


    filepath = file.get_audiofile_path()


    name = filepath.split('/')
    name = name[-1]

    dataset_path = os.path.join(filepath) 
    wavedata = os.path.join(dataset_path)
        
    sampleRate, audioBuffer = scipy.io.wavfile.read(wavedata)

    duracao = len(audioBuffer)/sampleRate


    tempo = np.arange(0,duracao,1/sampleRate)
            
    fig = plt.figure(figsize=(5,5), dpi=100)

    a = fig.add_subplot(111)

    a.plot(tempo, audioBuffer/10000)

    plt.xlabel('Tempo [s]')
    plt.ylabel('Amplitude [Hz]')
    plt.title(name)

    try:
        os.makedirs('./figures')
    except:
        pass

    my_path = './figures'
    name = name.split('.')
    my_file = name[0] + '.png'
        
    plt.savefig(os.path.join(my_path,my_file))


    file.set_imagefile_path(os.path.join(my_path,my_file))

    str_mensagem = "Salvo como " + name[0]

    mb.showinfo(title = "Aúdio Gravado!", message = str_mensagem)

    print('Gravação finalizada')




def stop(wait):
    tocar.switch_on(False)
    tocar.stop_timer()

    
    if wait:
        time.sleep(1)

    plt.close()
    #window.destroy()

    
def run_thread(thread, func, *args):
    if args:
        thread = threading.Thread(target=func, args=(args[0],)).start()
    else:
        thread = threading.Thread(target=func).start()
            

def run_daemon(thread, func, *args):
    if args:
        thread = threading.Thread(target=func, args=(args[0],))
    else:
        thread = threading.Thread(target=func).start()
    
    thread.setDaemon(True)
    thread.start()

def changeLabel(texto):
    textoGravando.set(texto)


    thread1 = ''
    thread2 = ''

def timer(root):
    label = Label(root, text= "Janela aberta com o botão")
    label.grid(column=0, row=3)

    #root.event_generate('<<vasco>>')
    

    start_time = time.time()
    lap_time = start_time

    while tocar.get_timer():
        lap_time = round(time.time() - start_time)
        total_time = str(lap_time)
        print(total_time)
        #label.config(text=total_time)
        time.sleep(1)

   

    