from entidade.pagamento import Pagamento
from entidade.pessoa import Pessoa


class Pix(Pagamento):
    def __init__(self, codigo: int, valor: float, pessoa: Pessoa, data: str, cpf: int):
        super().__init__(codigo, valor, pessoa, data)
        self.__cpf = None
        if isinstance(cpf, int):
            self.__cpf = cpf
 
    @property
    def cpf(self):
        return self.__cpf
        
    @cpf.setter
    def cpf(self, cpf: int):
        if isinstance(cpf, int):
            self.__cpf = cpf
            
    def get_metodo(self):
        return "PIX"

    def __str__(self):
        return f"PIX -  Código: {self.codigo} - Valor: R$ {self.valor:.2f} | Pessoa: {self.pessoa.nome} | Data: {self.data} | CPF: {self.cpf}"
        
