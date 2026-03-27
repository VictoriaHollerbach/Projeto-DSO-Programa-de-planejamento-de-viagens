class Pessoa:
    def __init__(self, nome: str, celular: int, identificacao: int, idade: int):
        self.__nome = None
        self.__celular = None
        self.__identificacao = None
        self.__idade = None
        if isinstance(identificacao, int):
            self.__identificacao = identificacao
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(celular, int):
            self.__celular = celular
        if isinstance(idade, int):
            self.__idade = idade

    @property
    def nome(self):
        return self.__nome
        
    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome
            
    @property
    def celular(self):
        return self.__celular
        
    @celular.setter
    def celular(self, celular: int):
        if isinstance(celular, int):
            self.__celular = celular
            
    @property
    def identificacao(self):
        return self.__identificacao
        
    @identificacao.setter
    def identificacao(self, identificacao: int):
        if isinstance(identificacao, int):
            self.__identificacao = identificacao


    @property
    def idade(self):
        return self.__idade
        
    @idade.setter
    def idade(self, idade: int):
        if isinstance(idade, int):
            self.__idade = idade


    def __str__(self):
        return f'Nome: {self.__nome} | Celular: {self.__celular} | Identificacao: {self.__identificacao} | Idade: {self.__idade}'

