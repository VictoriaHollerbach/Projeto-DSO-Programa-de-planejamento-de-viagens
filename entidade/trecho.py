from entidade.transporte import Transporte
from entidade.empresa import Empresa
from entidade.local import Local


class Trecho:
    def __init__(self, codigo: int, data: str, origem: Local, destino: Local, transporte: Transporte, 
                 empresa: Empresa, valor_trecho: float):
        self.__codigo = None
        if isinstance(codigo, int):
            self.__codigo = codigo
        self.__data = None
        if isinstance(data, str):
            self.__data = data
        self.__origem = None
        if isinstance(origem, Local):
            self.__origem = origem
        self.__destino = None
        if isinstance(destino, Local):
            self.__destino = destino
        self.__transporte = None
        if isinstance(transporte, Transporte):
            self.__transporte = transporte
        self.__empresa = None
        if isinstance(empresa, Empresa):
            self.__empresa = empresa
        self.__valor_trecho = None
        if isinstance(valor_trecho, float):
            self.__valor_trecho = valor_trecho

    @property
    def codigo(self):
        return self.__codigo
    
    @codigo.setter
    def codigo(self, codigo: int):
        if isinstance(codigo, int):
            self.__codigo = codigo

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data: str):
        if isinstance(data, str):
            self.__data = data
    
    @property
    def origem(self):
        return self.__origem
    
    @origem.setter
    def origem(self, origem: Local):
        if isinstance(origem, Local):
            self.__origem = origem
    
    @property
    def destino(self):
        return self.__destino
    
    @destino.setter
    def destino(self, destino: Local):
        if isinstance(destino, Local):
            self.__destino = destino

    @property
    def transporte(self):
        return self.__transporte
    
    @transporte.setter
    def transporte(self, transporte: Transporte):
        if isinstance(transporte, Transporte):
            self.__transporte = transporte
    
    @property
    def empresa(self):
        return self.__empresa
    
    @empresa.setter
    def empresa(self, empresa: Empresa):
        if isinstance(empresa, Empresa):
            self.__empresa = empresa

    @property
    def valor_trecho(self):
        return self.__valor_trecho

    @valor_trecho.setter
    def valor_trecho(self, valor_trecho: float):
        if isinstance(valor_trecho, float):
            self.__valor_trecho = valor_trecho 
            
    def __str__(self):
        return f"TRECHO - Código: {self.__codigo} | Data: {self.__data} | Origem: {self.__origem.cidade} - {self.__origem.pais} | Destino: {self.__destino.cidade} - {self.__destino.pais}| Transporte - {self.__transporte} - {self.__empresa.nome} | Valor: R$ {self.__valor_trecho:.2f}"
        
        
