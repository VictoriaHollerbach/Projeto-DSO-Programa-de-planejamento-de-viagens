from DAO.dao import DAO
from entidade.viagem import Viagem


class ViagemDAO(DAO):
    def __init__(self):
        super().__init__('viagens.pkl')

    def add(self, viagem: Viagem):
        if((viagem is not None) and isinstance(viagem, Viagem) and isinstance(viagem.codigo, int)):
            super().add(viagem.codigo, viagem)

    def update(self, viagem: Viagem):
        if((viagem is not None) and isinstance(viagem, Viagem) and isinstance(viagem.codigo, int)):
            super().update(viagem.codigo, viagem)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)
