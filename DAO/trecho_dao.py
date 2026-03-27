from DAO.dao import DAO
from entidade.trecho import Trecho


class TrechoDAO(DAO):
    def __init__(self):
        super().__init__('trechos.pkl')

    def add(self, trecho: Trecho):
        if((trecho is not None) and isinstance(trecho, Trecho) and isinstance(trecho.codigo, int)):
            super().add(trecho.codigo, trecho)

    def update(self, trecho: Trecho):
        if((trecho is not None) and isinstance(trecho, Trecho) and isinstance(trecho.codigo, int)):
            super().update(trecho.codigo, trecho)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)
