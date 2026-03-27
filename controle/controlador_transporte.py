from limite.tela_transporte import TelaTransporte
from entidade.transporte import Transporte
from DAO.transporte_dao import TransporteDAO

class ControladorTransportes():
    def __init__(self, controlador_sistema):
        self.__tela_transporte = TelaTransporte(self)
        self.__controlador_sistema = controlador_sistema
        self.__transporte_DAO = TransporteDAO()
    
    @property
    def transporte_DAO(self):
        return self.__transporte_DAO
    
    def find_transporte(self, tipo: str):
        for transporte in self.__transporte_DAO.get_all():
            if transporte.tipo == tipo:
                return transporte
        return None
    
    def _seleciona_transporte_obj(self):
        transportes = list(self.__transporte_DAO.get_all())
        
        if not transportes:
            self.__tela_transporte.mostra_mensagem("ERRO: Não há nenhum transporte cadastrado no sistema.")
            return None

        lista_formatada = []
        for t in transportes:
            # Assumindo que o __str__ ou propriedade principal é o tipo
            lista_formatada.append(t.tipo)

        tipo = self.__tela_transporte.seleciona_transporte_integrado(lista_formatada)
        
        if tipo is None:
            return None
        
        transporte = self.find_transporte(tipo)
        if transporte is None:
            self.__tela_transporte.mostra_mensagem("ERRO: Transporte não encontrado.")
            return None
        return transporte
    
    def incluir_transporte(self):
        dados_transporte = self.__tela_transporte.pega_dados_transporte()
        if dados_transporte is None: 
            return None
        
        transporte = self.find_transporte(dados_transporte['tipo'])
        if transporte is not None:
            self.__tela_transporte.mostra_mensagem('Erro: esse transporte já foi criado.')
            return None
        
        novo_transporte = Transporte(dados_transporte['tipo'])
        self.__transporte_DAO.add(novo_transporte)
        self.__tela_transporte.mostra_mensagem('Transporte incluído com sucesso!')
    
    def excluir_transporte(self):
        transporte_a_remover = self._seleciona_transporte_obj()
        if transporte_a_remover is not None:
            self.__transporte_DAO.remove(transporte_a_remover.tipo)
            self.__tela_transporte.mostra_mensagem('Transporte removido com sucesso!')
    
    def listar_transportes(self):
        transportes = self.__transporte_DAO.get_all()
        if not transportes:
            self.__tela_transporte.mostra_mensagem("Nenhum transporte registrado.")
            return
        
        titulo = "--- Lista de Transportes Registrados ---"
        lista_de_strings = [titulo]
        for transporte in transportes:
            lista_de_strings.append(str(transporte))
        
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_transporte.mostra_lista_scroll("Lista de Transportes", texto_completo)
    
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.incluir_transporte,
            2: self.excluir_transporte,
            3: self.listar_transportes
        }
        while True:
            opcao = self.__tela_transporte.mostra_tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao]
            funcao_escolhida()
