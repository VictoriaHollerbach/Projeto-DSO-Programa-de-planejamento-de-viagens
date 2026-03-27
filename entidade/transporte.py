from entidade.empresa import Empresa

class Transporte():
    def __init__(self, tipo: str):
        self.__tipo = None
        if isinstance(tipo, str):
            self.__tipo = tipo
            
    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, tipo: str):
        if isinstance(tipo, str):
            self.__tipo = tipo
        
    def __str__(self):
        return f'tipo: {self.__tipo}'
