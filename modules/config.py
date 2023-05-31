#Classe para guardar algumas configurações da aplicação
class config():
    
    def __init__(self, device = 0):
        self.device = device

    #implementar banco de dados
    def set_device(self, device):
        self.device = device
