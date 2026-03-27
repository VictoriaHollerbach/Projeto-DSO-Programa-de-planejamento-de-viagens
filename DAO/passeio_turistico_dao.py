from DAO.dao import DAO
from entidade.passeio_turistico import PasseioTuristico


class PasseioTuristicoDAO(DAO):
    def __init__(self):
        super().__init__('passeios_turisticos.pkl')

    def add(self, passeio_turistico: PasseioTuristico):
        if((passeio_turistico is not None) and isinstance(passeio_turistico, PasseioTuristico) and isinstance(passeio_turistico.atracao_turistica, str)):
            super().add(passeio_turistico.atracao_turistica, passeio_turistico)

    def update(self, passeio_turistico: PasseioTuristico):
        if((passeio_turistico is not None) and isinstance(passeio_turistico, PasseioTuristico) and isinstance(passeio_turistico.atracao_turistica, str)):
            super().update(passeio_turistico.atracao_turistica, passeio_turistico)

    def get(self, key):
        return super().get(key)

    def remove(self, key):
        return super().remove(key)
