import time


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton)

from modules.dialogo import salvoDialog

from modules.canvas import Canvas

import queue

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 
from matplotlib.animation import FuncAnimation

import sounddevice as sd

#Janela de gráfico dos arquivos externos
class signalWindow(QWidget):


            
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setWindowTitle('Sinal live')

        self.label = QLabel('Sinal Live')


        layout.addWidget(self.label) 

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

        

        canvas = FigureCanvasQTAgg(fig)
        ani  = FuncAnimation(fig,update_plot, interval=interval,blit=True)
        
        
        
        canvas.draw()


        plt.ylabel("Amplitude")    

        
        layout.addWidget(canvas)


        with stream:
            plt.show() 
          
        
      

        self.setLayout(layout)