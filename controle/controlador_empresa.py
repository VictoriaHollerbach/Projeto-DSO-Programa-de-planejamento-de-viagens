from limite.tela_empresa import TelaEmpresa
from entidade.empresa import Empresa
from DAO.empresa_dao import EmpresaDAO

class ControladorEmpresas():
    def __init__(self, controlador_sistema):
        self.__tela_empresa = TelaEmpresa(self)
        self.__empresa_DAO = EmpresaDAO()
        self.__controlador_sistema = controlador_sistema
    
    @property
    def empresa_DAO(self):
        return self.__empresa_DAO
    
    def _seleciona_empresa_obj(self):
        empresas = list(self.__empresa_DAO.get_all())
        
        if not empresas:
            self.__tela_empresa.mostra_mensagem("ERRO: Não há nenhuma empresa cadastrada no sistema.")
            return None

        lista_formatada = []
        for e in empresas:
            lista_formatada.append(f"CNPJ: {e.cnpj} | Nome: {e.nome}")

        cnpj = self.__tela_empresa.seleciona_empresa_integrada(lista_formatada)
        
        if cnpj is None:
            return None
        
        empresa = self.__empresa_DAO.get(cnpj)
        if empresa is None:
            self.__tela_empresa.mostra_mensagem("ERRO: Empresa não encontrada.")
            return None
        return empresa
    
    def incluir_empresa(self):
        dados_empresa = self.__tela_empresa.pega_dados_empresa()
        if dados_empresa is None:
            return
        cnpj = dados_empresa['cnpj']
        empresa = self.__empresa_DAO.get(cnpj)
        if empresa is None:
            nova_empresa = Empresa(dados_empresa['nome'], dados_empresa['cnpj'],
                                   dados_empresa['telefone'])
            self.__empresa_DAO.add(nova_empresa)
            self.__tela_empresa.mostra_mensagem("Empresa cadastrada com sucesso!")
        else:
            self.__tela_empresa.mostra_mensagem("Erro: Essa empresa já está cadastrada!")
        return None

    def excluir_empresa(self):
        empresa_a_remover = self._seleciona_empresa_obj()
        if empresa_a_remover is not None:
            self.__empresa_DAO.remove(empresa_a_remover.cnpj)
            self.__tela_empresa.mostra_mensagem('Empresa removida com sucesso!')
    
    def alterar_empresa(self):
        empresa = self._seleciona_empresa_obj()
        if empresa is not None:
            novos_dados = self.__tela_empresa.pega_dados_empresa()
            if novos_dados is None:
                return
            empresa.nome = novos_dados['nome']
            empresa.cnpj = novos_dados['cnpj']
            empresa.telefone = novos_dados['telefone']
            self.__empresa_DAO.update(empresa)
            self.listar_empresas()

    def listar_empresas(self):
        empresas = self.__empresa_DAO.get_all()
        if not empresas:
            self.__tela_empresa.mostra_mensagem("Nenhuma empresa registrada.")
            return
        titulo = "--- Lista de Empresas Registradas ---"
        lista_de_strings = [titulo]
        for empresa in empresas:
            lista_de_strings.append(str(empresa))
        texto_completo = "\n\n".join(lista_de_strings)
        self.__tela_empresa.mostra_lista_scroll("Lista de Empresas", texto_completo)
            
    def retornar(self):
        self.__controlador_sistema.abre_tela()
        
    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.incluir_empresa,
            2: self.excluir_empresa,
            3: self.alterar_empresa,
            4: self.listar_empresas
        }
        while True:
            opcao = self.__tela_empresa.mostra_tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao]
            funcao_escolhida()
