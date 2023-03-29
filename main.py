from tkinter import *
from tkinter import ttk
import sys 
sys.path.append('./modules')
from modules import functions


print(sys.path)

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

'''

label_file_explorer = Label(root,text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue")



button_show = Button(root, text='Exibir figuras salvas', command= showFigures)

button_record = Button(root, text='Gravar áudio', command=recordAudio)


'''


button_explore = Button(root, text = "Abrir arquivo", command = functions.browseFiles)
button_exit = Button(root, text="Sair", command=exit)




'''
label_file_explorer.grid(column = 0, row = 1)
  

button_show.grid(column=0, row=3)

button_record.grid(column=0, row=4)


'''





button_explore.pack()
  

button_exit.pack()

'''
button_record.grid(column=0, row = 0)
button_pause.grid(column=0, row = 1)
button_stop.grid(column=0, row = 2)



button_explore.grid(column = 1, row = 2)
  

button_exit.grid(column = 1,row = 5)
'''




functions.recorder(root)

functions.recordAudio(root)


root.mainloop()

