from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QVBoxLayout, QLabel)

class confirmDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excluir?")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    

        self.layout = QVBoxLayout()
        message = QLabel("Deseja excluir o registro?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)