from DAO.dao import DAO
from entidade.transporte import Transporte


class TransporteDAO(DAO):
    def __init__(self):
        super().__init__('transportes.pkl')

    def add(self, transporte: Transporte):
        if((transporte is not None) and isinstance(transporte, Transporte) and isinstance(transporte.tipo, str)):
            super().add(transporte.tipo, transporte)

    def update(self, transporte: Transporte):
        if((transporte is not None) and isinstance(transporte, Transporte) and isinstance(transporte.tipo, str)):
            super().update(transporte.tipo, transporte)

    def get(self, key):
        return super().get(key)

    def remove(self, key):
        return super().remove(key)
