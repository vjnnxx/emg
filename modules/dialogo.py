from PySide6.QtWidgets import (QMessageBox)
from PySide6.QtGui import QIcon


class salvoDialog(QMessageBox):

    


    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icon.png'))

        self.setWindowIconText("OK!")

        self.setWindowTitle('Tudo certo!')


        
        self.setText('Registro Salvo com sucesso!')

        self.setIcon(QMessageBox.Information)

        button = self.exec_()

        if button == QMessageBox.Ok:
            print("OK!")
        
        