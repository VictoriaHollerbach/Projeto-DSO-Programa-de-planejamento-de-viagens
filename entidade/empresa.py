class Empresa():
    def __init__(self, nome: str, cnpj: int, telefone: int):
        self.__nome = None
        if isinstance(nome, str):
            self.__nome = nome
        self.__cnpj = None
        if isinstance(cnpj, int):
            self.__cnpj = cnpj
        self.__telefone = None
        if isinstance(telefone, int):
            self.__telefone = telefone
        
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome
        
    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, cnpj: int):
        if isinstance(cnpj, int):
            self.__cnpj = cnpj
        
    @property
    def telefone(self):
        return self.__telefone
    
    @telefone.setter
    def telefone(self, telefone: int):
        if isinstance(telefone, int):
            self._telefone = telefone
    
    def __str__(self):
        return f"Empresa: {self.nome} | CNPJ: {self.cnpj} | Telefone: {self.telefone}"
