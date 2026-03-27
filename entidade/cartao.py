from entidade.pagamento import Pagamento
from entidade.pessoa import Pessoa


class Cartao(Pagamento):
    def __init__(self, codigo: int, valor: float, pessoa: Pessoa, data: str, numero_cartao: str,
                 bandeira: str):
        super().__init__(codigo, valor, pessoa, data)
        self.__numero_cartao = None
        if isinstance(numero_cartao, int):
            self.__numero_cartao = numero_cartao
        self.__bandeira = None
        if isinstance(bandeira, str):
            self.__bandeira = bandeira

    @property
    def numero_cartao(self):
        return self.__numero_cartao
        
    @numero_cartao.setter
    def numero_cartao(self, numero_cartao: int):
        if isinstance(numero_cartao, int):
            self.__numero_cartao = numero_cartao
            
    @property
    def bandeira(self):
        return self.__bandeira
        
    @bandeira.setter
    def bandeira(self, bandeira: str):
        if isinstance(bandeira, str):
            self.__bandeira = bandeira

    def get_metodo(self):
        return "CARTAO"
        
    def __str__(self):
        return f"CARTÃO - Código: {self.codigo} - Valor: R$ {self.valor:.2f} | Pessoa: {self.pessoa.nome} | Data: {self.data} | Bandeira: {self.bandeira}"
