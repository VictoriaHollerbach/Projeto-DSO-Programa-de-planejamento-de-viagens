from DAO.dao import DAO
from entidade.pagamento import Pagamento


class PagamentoDAO(DAO):
    def __init__(self):
        super().__init__('pagamentos.pkl')

    def add(self, pagamento: Pagamento):
        if((pagamento is not None) and isinstance(pagamento, Pagamento) and isinstance(pagamento.codigo, int)):
            super().add(pagamento.codigo, pagamento)

    def update(self, pagamento: Pagamento):
        if((pagamento is not None) and isinstance(pagamento, Pagamento) and isinstance(pagamento.codigo, int)):
            super().update(pagamento.codigo, pagamento)

    def get(self, key:int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key:int):
        if(isinstance(key, int)):
            return super().remove(key)
