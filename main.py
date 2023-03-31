from tkinter import *
from tkinter import ttk

import threading
import sys 
sys.path.append('./modules')
from modules.functions import *


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


button_explore = Button(root, text = "Abrir arquivo", command = browseFiles)
button_exit = Button(root, text="Sair", command=exit)



button_explore.pack()
  

button_exit.pack()


recorder(root)
recordAudio(root)


root.mainloop()

