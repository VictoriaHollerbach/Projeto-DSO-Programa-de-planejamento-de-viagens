from DAO.dao import DAO
from entidade.pessoa import Pessoa


class PessoaDAO(DAO):
    def __init__(self):
        super().__init__('pessoas.pkl')

    def add(self, pessoa: Pessoa):
        if((pessoa is not None) and isinstance(pessoa, Pessoa) and isinstance(pessoa.identificacao, int)):
            super().add(pessoa.identificacao, pessoa)

    def update(self, pessoa:Pessoa):
        if((pessoa is not None) and isinstance(pessoa, Pessoa) and isinstance(pessoa.identificacao, int)):
            super().update(pessoa.identificacao, pessoa)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)
