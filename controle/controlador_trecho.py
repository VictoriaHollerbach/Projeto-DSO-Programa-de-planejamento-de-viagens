from entidade.trecho import Trecho
from limite.tela_trecho import TelaTrecho
from DAO.trecho_dao import TrechoDAO

class ControladorTrechos():
    def __init__(self, controlador_sistema):
        self.__tela_trecho = TelaTrecho(self)
        self.__trecho_DAO = TrechoDAO()
        self.__controlador_sistema = controlador_sistema

    @property
    def trecho_DAO(self):
        return self.__trecho_DAO
        
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema
    
    def find_trecho_no_sistema(self, codigo: int):
        for trecho in self.__trecho_DAO.get_all():
            if trecho.codigo == codigo:
                return trecho
        return None
    
    def find_trecho_na_viagem(self, viagem, codigo: int):
        for trecho in viagem.trechos:
            if trecho.codigo == codigo:
                return trecho
        return None
    
    # --- Helpers de Seleção ---
    def _seleciona_viagem_obj(self):
        viagens = list(self.controlador_sistema.controlador_viagens.viagem_DAO.get_all())
        if not viagens:
            self.__tela_trecho.mostra_mensagem("ERRO: Não há viagens cadastradas.")
            return None
        lista = [f"Cód: {v.codigo} | Nome: {v.nome_viagem}" for v in viagens]
        codigo = self.__tela_trecho.seleciona_viagem_integrada(lista)
        if codigo is None: return None
        return self.controlador_sistema.controlador_viagens.find_viagem_by_codigo(codigo)

    def _seleciona_local_obj(self, titulo):
        locais = list(self.controlador_sistema.controlador_locais.local_DAO.get_all())
        if not locais:
            self.__tela_trecho.mostra_mensagem(f"ERRO: Não há locais cadastrados para selecionar {titulo}.")
            return None
        lista = [f"Cidade: {l.cidade} | País: {l.pais}" for l in locais]
        cidade = self.__tela_trecho.seleciona_local_integrado(lista, titulo)
        if cidade is None: return None
        return self.controlador_sistema.controlador_locais.find_local_by_cidade(cidade)

    def _seleciona_transporte_obj(self):
        transportes = list(self.controlador_sistema.controlador_transportes.transporte_DAO.get_all())
        if not transportes:
            self.__tela_trecho.mostra_mensagem("ERRO: Não há transportes cadastrados.")
            return None
        lista = [t.tipo for t in transportes]
        tipo = self.__tela_trecho.seleciona_transporte_integrado(lista)
        if tipo is None: return None
        return self.controlador_sistema.controlador_transportes.find_transporte(tipo)

    def _seleciona_empresa_obj(self):
        empresas = list(self.controlador_sistema.controlador_empresas.empresa_DAO.get_all())
        if not empresas:
            self.__tela_trecho.mostra_mensagem("ERRO: Não há empresas cadastradas.")
            return None
        lista = [f"CNPJ: {e.cnpj} | Nome: {e.nome}" for e in empresas]
        cnpj = self.__tela_trecho.seleciona_empresa_integrada(lista)
        if cnpj is None: return None
        return self.controlador_sistema.controlador_empresas.empresa_DAO.get(cnpj)

    def _seleciona_trecho_obj(self, viagem):
        if not viagem.trechos:
            self.__tela_trecho.mostra_mensagem("ERRO: Esta viagem não possui trechos.")
            return None
        lista = [f"Trecho Cód: {t.codigo} | Origem: {t.origem.cidade} -> Destino: {t.destino.cidade}" for t in viagem.trechos]
        codigo = self.__tela_trecho.seleciona_trecho_integrado(lista)
        if codigo is None: return None
        return self.find_trecho_na_viagem(viagem, codigo)

    # --- CRUD ---
    def incluir_trecho(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None: return

        origem = self._seleciona_local_obj("Selecionar Origem")
        if origem is None: return

        destino = self._seleciona_local_obj("Selecionar Destino")
        if destino is None: return

        transporte = self._seleciona_transporte_obj()
        if transporte is None: return

        empresa = self._seleciona_empresa_obj()
        if empresa is None: return

        dados_simples = self.__tela_trecho.pega_dados_trecho_simples()
        if dados_simples is None: return

        trecho = self.find_trecho_na_viagem(viagem, dados_simples['codigo'])
        if trecho is None:
            novo_trecho = Trecho(dados_simples['codigo'], dados_simples['data'], origem, destino,
                                 transporte, empresa, dados_simples['valor_trecho'])
            viagem.trechos.append(novo_trecho)
            self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
            
            if novo_trecho not in self.__trecho_DAO.get_all():
                self.__trecho_DAO.add(novo_trecho)
            self.__tela_trecho.mostra_mensagem('Trecho incluído com sucesso!')
        else:
            self.__tela_trecho.mostra_mensagem('Erro: esse trecho já foi criado nesta viagem.')

    def excluir_trecho(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None: return

        trecho_a_remover = self._seleciona_trecho_obj(viagem)
        if trecho_a_remover is not None:
            viagem.trechos.remove(trecho_a_remover)
            self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
            try:
                self.__trecho_DAO.remove(trecho_a_remover.codigo)
            except:
                pass
            self.__tela_trecho.mostra_mensagem('Trecho removido com sucesso!')
        else:
            self.__tela_trecho.mostra_mensagem('Erro: Trecho não encontrado.')

    def alterar_trecho(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None: return

        trecho = self._seleciona_trecho_obj(viagem)
        if trecho is not None:
            # Seleciona novos objetos (opcional: poderia manter os antigos se o usuário cancelar, mas aqui obrigamos a re-seleção para garantir integridade)
            nova_origem = self._seleciona_local_obj("Nova Origem")
            if nova_origem is None: return
            
            novo_destino = self._seleciona_local_obj("Novo Destino")
            if novo_destino is None: return
            
            novo_transporte = self._seleciona_transporte_obj()
            if novo_transporte is None: return
            
            nova_empresa = self._seleciona_empresa_obj()
            if nova_empresa is None: return

            novos_dados = self.__tela_trecho.pega_dados_trecho_simples()
            if novos_dados is None: return

            # Atualiza
            trecho.codigo = novos_dados['codigo']
            trecho.data = novos_dados['data']
            trecho.valor_trecho = novos_dados['valor_trecho']
            trecho.origem = nova_origem
            trecho.destino = novo_destino
            trecho.transporte = novo_transporte
            trecho.empresa = nova_empresa

            self.controlador_sistema.controlador_viagens.atualiza_viagem(viagem)
            # Atualiza no DAO global se necessário (assumindo update simples)
            # self.__trecho_DAO.update(trecho) 
            
            self.__tela_trecho.mostra_mensagem('Trecho alterado com sucesso!')
            self.listar_trechos(viagem)
        else:
            self.__tela_trecho.mostra_mensagem('Erro: Trecho não encontrado.')

    def listar_trechos_na_viagem(self):
        viagem = self._seleciona_viagem_obj()
        if viagem is None: return
        self.listar_trechos(viagem)

    def listar_trechos(self, viagem):
        titulo = f"--- Trechos da Viagem {viagem.nome_viagem} ---"
        if not viagem.trechos:
            self.__tela_trecho.mostra_mensagem("Nenhum trecho registrado.")
            return
        
        lista = [titulo]
        for trecho in viagem.trechos:
            lista.append(str(trecho))
        
        texto = "\n\n".join(lista)
        self.__tela_trecho.mostra_lista_scroll("Lista de Trechos", texto)

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            0: self.retornar,
            1: self.incluir_trecho,
            2: self.excluir_trecho,
            3: self.alterar_trecho,
            4: self.listar_trechos_na_viagem
        }
        while True:
            opcao = self.__tela_trecho.mostra_tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao]
            funcao_escolhida()
