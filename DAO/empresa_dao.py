from DAO.dao import DAO
from entidade.empresa import Empresa


class EmpresaDAO(DAO):
    def __init__(self):
        super().__init__('empresas.pkl')

    def add(self, empresa: Empresa):
        if((empresa is not None) and isinstance(empresa, Empresa) and isinstance(empresa.cnpj, int)):
            super().add(empresa.cnpj, empresa)

    def update(self, empresa: Empresa):
        if((empresa is not None) and isinstance(empresa, Empresa) and isinstance(empresa.cnpj, int)):
            super().update(empresa.cnpj, empresa)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)
