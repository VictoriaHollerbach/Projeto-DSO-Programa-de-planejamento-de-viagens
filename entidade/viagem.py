class Viagem():
    def __init__(self, codigo: int, nome_viagem: str, data_inc: str, data_fim: str):
        self.__codigo = None
        if isinstance(codigo, int):
            self.__codigo = codigo
        self.__nome_viagem = None
        if isinstance(nome_viagem, str):
            self.__nome_viagem = nome_viagem
        self.__data_inc = None
        if isinstance(data_inc, str):
            self.__data_inc = data_inc
        self.__data_fim = None
        if isinstance(data_fim, str):
            self.__data_fim = data_fim
        self.__pessoas = []
        self.__passeios_turisticos = []
        self.__trechos = []
        self.__pagamentos = []
    
    @property
    def codigo(self):
        return self.__codigo
    
    @codigo.setter
    def codigo(self, codigo):
        if isinstance(codigo, int):
            self.__codigo = codigo

    @property
    def nome_viagem(self):
        return self.__nome_viagem
    
    @nome_viagem.setter
    def nome_viagem(self, nome_viagem: str):
        if isinstance(nome_viagem, str):
            self.__nome_viagem = nome_viagem

    @property
    def data_inc(self):
        return self.__data_inc

    @data_inc.setter
    def data_inc(self, data_inc):
        if isinstance(data_inc, str):
            self.__data_inc = data_inc

    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, data_fim):
        if isinstance(data_fim, str):
            self.__data_fim = data_fim

    @property
    def pessoas(self):
        return self.__pessoas
    
    @property
    def passeios_turisticos(self):
        return self.__passeios_turisticos
    
    @property
    def trechos(self):
        return self.__trechos
    
    @property
    def pagamentos(self):
        return self.__pagamentos
    
    def __str__(self):
        return f"Viagem: {self.nome_viagem} | Código: {self.codigo} | Data de Início: {self.data_inc} | Data de Fim: {self.data_fim}"
        


