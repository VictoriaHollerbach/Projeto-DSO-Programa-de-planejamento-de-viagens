from abc import ABC, abstractmethod
from entidade.pessoa import Pessoa


class Pagamento(ABC):
    @abstractmethod
    def __init__(self, codigo: int, valor: float, pessoa: Pessoa, data: str):
        self.__codigo = None
        if isinstance(codigo, int):
            self.__codigo = codigo
        self.__valor = None
        if isinstance(valor, (float, int)):
            self.__valor = float(valor)
        self.__pessoa = None
        if isinstance(pessoa, Pessoa):
            self.__pessoa = pessoa
        self.__data = None
        if isinstance(data, str):
            self.__data = data
        
    @property
    def codigo(self):
        return self.__codigo
    
    @codigo.setter
    def codigo(self, codigo: int):
        if isinstance(codigo, int):
            self.__codigo = codigo


    @property
    def valor(self):
        return self.__valor
    
    @valor.setter
    def valor(self, valor: float):
        if isinstance(valor, (float, int)) and valor > 0:
            self.__valor = float(valor)
        else:
            raise ValueError("Valor do pagamento deve ser numérico e positivo.")
            
    @property
    def pessoa(self):
        return self.__pessoa
    @pessoa.setter
    def pessoa(self, pessoa: Pessoa):
        if isinstance(pessoa, Pessoa):
            self.__pessoa = pessoa
        else:
            raise TypeError("Pessoa deve ser uma instância da classe Pessoa.")
            
    @property
    def data(self):
        return self.__data
    @data.setter
    def data(self, data: str):
        if isinstance(data, str):
            self.__data = data
            
    @abstractmethod
    def get_metodo(self):
        pass

