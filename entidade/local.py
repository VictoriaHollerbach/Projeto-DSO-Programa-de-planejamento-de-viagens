class Local:
    def __init__(self, cidade: str, pais: str):
        self.__cidade = None
        self.__pais = None
        if isinstance(cidade, str):
            self.__cidade = cidade
        if isinstance(pais, str):
            self.__pais = pais
            
    @property
    def cidade(self):
        return self.__cidade
        
    @cidade.setter
    def cidade(self, cidade: str):
        if isinstance(cidade, str):
            self.__cidade = cidade
            
    @property
    def pais(self):
        return self.__pais

    @pais.setter
    def pais(self, pais: str):
        if isinstance(pais, str):
            self.__pais = pais

    def __str__(self):
        return f'Cidade: {self.__cidade} | Pais: {self.__pais}'
