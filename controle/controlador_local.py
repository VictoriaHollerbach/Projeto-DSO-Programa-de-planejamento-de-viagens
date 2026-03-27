from entidade.local import Local
from limite.tela_local import TelaLocal
from DAO.local_dao import LocalDAO

class ControladorLocais():
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__local_DAO = LocalDAO()
        self.__tela_local = TelaLocal(self)

    @property
    def local_DAO(self):
        return self.__local_DAO
    
    def find_local_by_cidade(self, cidade: str):
        for local in self.__local_DAO.get_all():
            if local.cidade == cidade:
                return local
        return None
    
    def _seleciona_local_obj(self):
        locais = list(self.__local_DAO.get_all())
        
        if not locais:
            self.__tela_local.mostra_mensagem("ERRO: Não há nenhum local cadastrado no sistema.")
            return None

        lista_formatada = []
        for l in locais:
            lista_formatada.append(f"Cidade: {l.cidade} | País: {l.pais}")

        cidade = self.__tela_local.seleciona_local_integrado(lista_formatada)
        
        if cidade is None:
            return None
        
        local = self.find_local_by_cidade(cidade)
        if local is None:
            self.__tela_local.mostra_mensagem("ERRO: Local não encontrado.")
            return None
        return local
    
    def incluir_local(self):
        dados_local = self.__tela_local.pega_dados_local()
        if dados_local is None:
            return
        
        cidade = dados_local['cidade']
        local = self.find_local_by_cidade(cidade)
        if local is None:
            novo_local = Local(dados_local['cidade'], dados_local['pais'])
            self.__local_DAO.add(novo_local)
            self.__tela_local.mostra_mensagem("Local cadastrado com sucesso!")
        else:
            self.__tela_local.mostra_mensagem("Erro: Esse local já está cadastrado!")
        return None
    
    def excluir_local(self):
        local_a_remover = self._seleciona_local_obj()
        if local_a_remover is not None:
            self.__local_DAO.remove(local_a_remover.cidade)
            self.__tela_local.mostra_mensagem('Local removido com sucesso!')
    
    def alterar_local(self):
        local = self._seleciona_local_obj()
        if local is not None:
            novos_dados = self.__tela_local.pega_dados_local()
            if novos_dados is None:
                return
            
            local.cidade = novos_dados['cidade']
            local.pais = novos_dados['pais']
            self.__local_DAO.update(local)
            self.listar_locais()

    def listar_locais(self):
        locais = self.__local_DAO.get_all()
        if not locais:
            self.__tela_local.mostra_mensagem("Nenhum local registrado.")
            return
        
        titulo = "--- Lista de Locais Registrados ---"
        lista_de_strings = [titulo]
        for local in locais:
            lista_de_strings.append(str(local))
            
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_local.mostra_lista_scroll("Lista de Locais", texto_completo)
    
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.incluir_local,
            2: self.excluir_local,
            3: self.alterar_local,
            4: self.listar_locais
        }
        while True:
            opcao = self.__tela_local.mostra_tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao]
            funcao_escolhida()
