from DAO.dao import DAO
from entidade.local import Local


class LocalDAO(DAO):
    def __init__(self):
        super().__init__('locais.pkl')

    def add(self, local: Local):
        if((local is not None) and isinstance(local, Local) and isinstance(local.cidade, str)):
            super().add(local.cidade, local)

    def update(self, local: Local):
        if((local is not None) and isinstance(local, Local) and isinstance(local.cidade, str)):
            super().update(local.cidade, local)

    def get(self, key):
        return super().get(key)

    def remove(self, key):
        return super().remove(key)
